from django.db import models

from apps.training.models import Training
from apps.users.models import User


class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('VIEW', 'Просмотр тренировки'),
        ('COMPLETE', 'Завершение тренировки'),
        ('CALL_START', 'Начало звонка'),
        ('CALL_END', 'Завершение звонка'),
        ('PRODUCT_VIEW', 'Просмотр товара'),
        ('PRODUCT_CLICK', 'Клик по товару')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    product = models.ForeignKey('product.Product', null=True, on_delete=models.SET_NULL)
    training = models.ForeignKey('training.Training', null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, blank=True)
    duration = models.PositiveIntegerField(null=True)