from collections import defaultdict

from django.shortcuts import render
from django.views import View

from movies.models import Movie


class RecommendationView(View):
    template_name = 'recommendations/index.html'

    def get(self, request):
        if request.user.is_authenticated and not request.user.is_new_user:
            from .engine import get_recommendations
            recommendations = get_recommendations(request.user.id, n=20)

            # Sort all by rating desc (5-star first)
            recommendations = sorted(recommendations, key=lambda m: m.avg_rating, reverse=True)

            # Group by primary genre, pick top 4 most-populated genres
            genre_groups = defaultdict(list)
            for movie in recommendations:
                genres = list(movie.genres.all())
                primary = genres[0].name if genres else 'Other'
                genre_groups[primary].append(movie)

            genre_sections = sorted(genre_groups.items(), key=lambda x: len(x[1]), reverse=True)[:4]

            context = {
                'genre_sections': genre_sections,
                'is_cold_start': False,
            }
        else:
            context = {
                'trending': Movie.objects.order_by('-total_watches')[:12],
                'top_rated': Movie.objects.order_by('-avg_rating')[:12],
                'new_releases': Movie.objects.order_by('-year', '-avg_rating')[:12],
                'is_cold_start': True,
            }
        return render(request, self.template_name, context)
