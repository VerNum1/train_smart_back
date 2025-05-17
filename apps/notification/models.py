from django.db import models

from apps.users.models import User


class Notification(models.Model):
    """Модель для хранения уведомлений пользователя"""
    TYPE_CHOICES = [
        ('CALL', 'Входящий звонок'),
        ('FRIEND_REQUEST', 'Запрос в друзья'),
        ('TRAINING_REMINDER', 'Напоминание о тренировке'),
        ('PRODUCT_RECOMMENDATION', 'Рекомендация товара')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES
    )
    message = models.TextField()
    related_training = models.ForeignKey(
        'Training',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    related_product = models.ForeignKey(
        'Product',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
