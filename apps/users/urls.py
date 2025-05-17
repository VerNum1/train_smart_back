from django.contrib import admin

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import UserProfileView, FriendshipViewSet

router = DefaultRouter()
router.register(r'friendships', FriendshipViewSet, basename='friendship')


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]