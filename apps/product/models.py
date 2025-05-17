from django.db import models

from apps.users.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('NUTRITION', 'Спортпит'),
        ('EQUIPMENT', 'Снаряжение'),
        ('CLOTHING', 'Одежда'),
        ('ACCESSORY', 'Аксессуары')  # new
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    store_links = models.JSONField()
    sport_types = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200)
    target_gender = models.CharField(
        max_length=1,
        choices=User.GENDER_CHOICES,
        default='M'
    )
    popularity_score = models.FloatField(default=0.0)
