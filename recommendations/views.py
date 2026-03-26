from django.shortcuts import render
from django.views import View

from movies.models import Movie


class RecommendationView(View):
    template_name = 'recommendations/index.html'

    def get(self, request):
        if request.user.is_authenticated and not request.user.is_new_user:
            # Existing user with rating history: use SVD recommendations
            from .engine import get_recommendations
            recommendations = get_recommendations(request.user.id, n=20)
            context = {
                'recommendations': recommendations,
                'is_cold_start': False,
            }
        else:
            # New user or anonymous: cold start recommendations
            context = {
                'trending': Movie.objects.order_by('-total_watches')[:12],
                'top_rated': Movie.objects.order_by('-avg_rating')[:12],
                'new_releases': Movie.objects.order_by('-year', '-avg_rating')[:12],
                'is_cold_start': True,
            }
        return render(request, self.template_name, context)
