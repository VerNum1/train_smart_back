from django.db import models

from apps.users.models import User


class Chat(models.Model):
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_p1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_p2')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.DateTimeField(null=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class MessageFile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='chat_files/')
    file_type = models.CharField(max_length=20)
