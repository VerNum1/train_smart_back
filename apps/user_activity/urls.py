from django.urls import path

from apps.user_activity.views import UserActivityView

urlpatterns = [
    path('activity/', UserActivityView.as_view(), name='user-activity'),
]
