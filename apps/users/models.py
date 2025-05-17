from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class User(AbstractUser):
    USER_ROLES = (("TRAINER", "Тренер"), ("USER", "Пользователь"))
    GENDER_CHOICES = [('M', 'Мужской'), ('F', 'Женский')]

    role = models.CharField(max_length=10, choices=USER_ROLES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    goal = models.CharField(max_length=100, blank=True, null=True)
    sport_type = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text='Группы, к которым принадлежит пользователь',
        related_name="custom_user_groups",  # Уникальное имя
        related_query_name="custom_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Права доступа',
        blank=True,
        help_text='Специфичные права для этого пользователя',
        related_name="custom_user_permissions",  # Уникальное имя
        related_query_name="custom_user",
    )
    REQUIRED_FIELDS = []


def validate_social_urls(value):
    validator = URLValidator()
    if isinstance(value, dict):
        for url in value.values():
            try:
                validator(url)
            except ValidationError:
                raise ValidationError(f"Invalid URL: {url}")
    return value


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainer_profile")
    bio = models.TextField()
    certificates = models.FileField(upload_to="certificates/")
    rating = models.FloatField(default=0.0)
    social_links = models.JSONField(
        verbose_name="Социальные сети",
        default=dict,
        blank=True,
        validators=[validate_social_urls]
    )


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(("PENDING", "В ожидании"), ("ACCEPTED", "Принято")))
    created_at = models.DateTimeField(auto_now_add=True)  # Добавлено для аналитики
