from rest_framework import generics, permissions

from apps.user_activity.models import UserActivity
from apps.user_activity.serializers import UserActivitySerializer


class UserActivityView(generics.ListAPIView):
    """История активности пользователя"""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)
