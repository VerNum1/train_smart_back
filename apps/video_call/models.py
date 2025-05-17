from django.db import models

from apps.users.models import User


class VideoCall(models.Model):
    STATUS_CHOICES = (("ONGOING", "Активен"), ("ENDED", "Завершен"))
    caller = models.ForeignKey(User, related_name="outgoing_calls", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="incoming_calls", on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    call_type = models.CharField(  # Новое поле
        max_length=10,
        choices=(("PRIVATE", "Личный"), ("GROUP", "Групповой"))
    )