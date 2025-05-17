from django.urls import path

from apps.chat.views import ChatListView, MessageFileUploadView, MarkMessageReadView

urlpatterns = [
    path('chats/', ChatListView.as_view(), name='chats'),
    path('messages/<int:message_id>/files/', MessageFileUploadView.as_view(), name='message-file-upload'),
    path('messages/<int:pk>/read/', MarkMessageReadView.as_view(), name="message-read"),
]
