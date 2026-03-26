from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from .forms import SearchForm
from .models import Genre, Movie, Watchlist, WatchHistory


class HomeView(View):
    template_name = 'movies/home.html'

    def get(self, request):
        context = {
            'featured_movies': Movie.objects.order_by('-avg_rating')[:8],
            'trending_movies': Movie.objects.order_by('-total_watches')[:8],
            'new_releases': Movie.objects.order_by('-year', '-avg_rating')[:8],
            'genres': Genre.objects.all().order_by('name'),
        }
        return render(request, self.template_name, context)


class MovieListView(View):
    template_name = 'movies/list.html'
    paginate_by = 20

    def get(self, request):
        movies = Movie.objects.all().prefetch_related('genres')
        form = SearchForm(request.GET)

        # Apply filters
        genre_id = request.GET.get('genre_id')
        q = request.GET.get('q', '').strip()
        year_from = request.GET.get('year_from')
        year_to = request.GET.get('year_to')
        min_rating = request.GET.get('min_rating')

        if q:
            movies = movies.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if genre_id:
            try:
                movies = movies.filter(genres__id=int(genre_id))
            except (ValueError, TypeError):
                pass

        if year_from:
            try:
                movies = movies.filter(year__gte=int(year_from))
            except (ValueError, TypeError):
                pass

        if year_to:
            try:
                movies = movies.filter(year__lte=int(year_to))
            except (ValueError, TypeError):
                pass

        if min_rating:
            try:
                movies = movies.filter(avg_rating__gte=float(min_rating))
            except (ValueError, TypeError):
                pass

        movies = movies.distinct()

        paginator = Paginator(movies, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        selected_genre = None
        if genre_id:
            try:
                selected_genre = Genre.objects.get(id=int(genre_id))
            except (Genre.DoesNotExist, ValueError, TypeError):
                pass

        context = {
            'page_obj': page_obj,
            'movies': page_obj,
            'genres': Genre.objects.all().order_by('name'),
            'selected_genre': selected_genre,
            'form': form,
            'query': q,
            'total_count': paginator.count,
        }
        return render(request, self.template_name, context)


class MovieDetailView(View):
    template_name = 'movies/detail.html'

    def get(self, request, pk):
        movie = get_object_or_404(Movie.objects.prefetch_related('genres', 'reviews__user'), pk=pk)

        from reviews.models import Review

        user_review = None
        in_watchlist = False

        if request.user.is_authenticated:
            user_review = Review.objects.filter(user=request.user, movie=movie).first()
            in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()

        reviews = movie.reviews.select_related('user').order_by('-created_at')[:10]
        related_movies = Movie.objects.filter(
            genres__in=movie.genres.all()
        ).exclude(pk=movie.pk).distinct()[:6]

        context = {
            'movie': movie,
            'reviews': reviews,
            'user_review': user_review,
            'in_watchlist': in_watchlist,
            'related_movies': related_movies,
            'genre_list': movie.genres.all(),
        }
        return render(request, self.template_name, context)


class SearchView(View):
    template_name = 'movies/search.html'
    paginate_by = 20

    def get(self, request):
        movies = Movie.objects.all().prefetch_related('genres')
        form = SearchForm(request.GET)

        q = request.GET.get('q', '').strip()
        genre_id = request.GET.get('genre_id')
        year_from = request.GET.get('year_from')
        year_to = request.GET.get('year_to')
        min_rating = request.GET.get('min_rating')

        if q:
            movies = movies.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if genre_id:
            try:
                movies = movies.filter(genres__id=int(genre_id))
            except (ValueError, TypeError):
                pass

        if year_from:
            try:
                movies = movies.filter(year__gte=int(year_from))
            except (ValueError, TypeError):
                pass

        if year_to:
            try:
                movies = movies.filter(year__lte=int(year_to))
            except (ValueError, TypeError):
                pass

        if min_rating:
            try:
                movies = movies.filter(avg_rating__gte=float(min_rating))
            except (ValueError, TypeError):
                pass

        movies = movies.distinct()

        paginator = Paginator(movies, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'movies': page_obj,
            'genres': Genre.objects.all().order_by('name'),
            'form': form,
            'query': q,
            'total_count': paginator.count,
        }
        return render(request, self.template_name, context)


class AddToWatchlistView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        watchlist_item, created = Watchlist.objects.get_or_create(
            user=request.user,
            movie=movie,
        )
        if not created:
            watchlist_item.delete()
            in_watchlist = False
            message = f'"{movie.title}" removed from your watchlist.'
        else:
            in_watchlist = True
            message = f'"{movie.title}" added to your watchlist.'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'in_watchlist': in_watchlist, 'message': message})

        messages.success(request, message)
        return redirect('movies:detail', pk=pk)


class RecordWatchView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        WatchHistory.objects.create(user=request.user, movie=movie)
        Movie.objects.filter(pk=pk).update(total_watches=movie.total_watches + 1)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'message': f'Marked "{movie.title}" as watched.'})

        messages.success(request, f'"{movie.title}" marked as watched.')
        return redirect('movies:detail', pk=pk)
