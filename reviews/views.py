from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from movies.models import Movie
from .forms import ReviewForm
from .models import Review
from .sentiment import analyze_sentiment


class AddReviewView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)

        # Check if user already reviewed this movie
        existing_review = Review.objects.filter(user=request.user, movie=movie).first()
        if existing_review:
            messages.warning(request, 'You have already reviewed this movie. Delete your existing review first.')
            return redirect('movies:detail', pk=movie_id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie

            # Run sentiment analysis
            review_text = form.cleaned_data.get('review_text', '')
            review.sentiment = analyze_sentiment(review_text)

            review.save()

            # Recalculate movie avg_rating from all reviews
            _update_movie_rating(movie)

            # Mark user as no longer new after first rating
            if request.user.is_new_user:
                request.user.is_new_user = False
                request.user.save(update_fields=['is_new_user'])

            # Auto-retrain SVD every 50 new reviews
            total_reviews = Review.objects.count()
            if total_reviews % 50 == 0:
                try:
                    from recommendations.engine import train_svd_model
                    train_svd_model()
                except Exception:
                    pass  # Non-blocking: retrain failure should not break review submission

            messages.success(request, f'Your review for "{movie.title}" has been posted!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

        return redirect('movies:detail', pk=movie_id)

    def get(self, request, movie_id):
        # Redirect GET requests to movie detail page
        return redirect('movies:detail', pk=movie_id)


class DeleteReviewView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        # Only the owner can delete their review
        if review.user != request.user and not request.user.is_staff:
            messages.error(request, 'You do not have permission to delete this review.')
            return redirect('movies:detail', pk=review.movie.pk)

        movie = review.movie
        movie_id = movie.pk
        review.delete()

        # Recalculate movie avg_rating after deletion
        _update_movie_rating(movie)

        messages.success(request, f'Your review for "{movie.title}" has been deleted.')
        return redirect('movies:detail', pk=movie_id)

    def get(self, request, pk):
        return redirect('home')


def _update_movie_rating(movie):
    """Recalculate and save movie avg_rating and total_ratings from all its reviews."""
    from django.db.models import Avg, Count
    stats = Review.objects.filter(movie=movie).aggregate(
        avg=Avg('rating'),
        count=Count('id'),
    )
    movie.avg_rating = round(stats['avg'] or 0.0, 2)
    movie.total_ratings = stats['count'] or 0
    movie.save(update_fields=['avg_rating', 'total_ratings'])
