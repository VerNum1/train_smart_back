from rest_framework import serializers

from apps.training.models import Training
from apps.users.serializers import BaseUserSerializer


class TrainingSerializer(serializers.ModelSerializer):
    created_by = BaseUserSerializer(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    difficulty = serializers.ChoiceField(choices=Training.DIFFICULTY_CHOICES)

    class Meta:
        model = Training
        fields = ["id", "title", "description", "category", "tags",
                "video_url", "duration", "created_by", "is_completed", "difficulty"]