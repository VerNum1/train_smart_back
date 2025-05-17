from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.training.views import TrainingViewSet

router = DefaultRouter()
router.register(r'trainings', TrainingViewSet, basename='training')

urlpatterns = [
    path('', include(router.urls)),
]
