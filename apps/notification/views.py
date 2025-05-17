from rest_framework import generics, permissions

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """Список уведомлений"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')