from django.urls import path

from apps.product.views import ProductRecommendationAPI

urlpatterns = [
    path('recommendations/', ProductRecommendationAPI.as_view(), name='recommendations'),
]