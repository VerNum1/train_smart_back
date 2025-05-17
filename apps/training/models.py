from django.db import models

from apps.users.models import User


# training.py
class Training(models.Model):
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Начинающий'),
        ('INTERMEDIATE', 'Средний'),
        ('ADVANCED', 'Продвинутый')
    ]
    TYPE_CHOICES = [
        ("KNOWLEDGE_BASE", "База знаний"),
        ("FULL_TRAININGS", "Полноценные тренировки")
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)  # Йога, кардио и т.д.
    video_url = models.URLField()
    duration = models.IntegerField()  # В минутах
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(
        max_length=12,
        choices=DIFFICULTY_CHOICES,
        default='BEGINNER'
    )
    tags = models.CharField(max_length=200)
    equipment_required = models.TextField(blank=True)
    type = models.CharField(
        max_length=14,
        choices=TYPE_CHOICES,
        default='FULL_TRAININGS'
    )


class TrainingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True)