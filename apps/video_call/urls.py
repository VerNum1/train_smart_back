from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.video_call.views import VideoCallViewSet

router = DefaultRouter()
router.register(r'calls', VideoCallViewSet, basename='videocall')

urlpatterns = [
    path('', include(router.urls)),
]
