from django.urls import path

from apps.notification.views import NotificationListView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]