from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from rest_framework import serializers

from apps.users.models import Friendship, TrainerProfile

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор без зависимостей от других приложений"""
    class Meta:
        model = User
        fields = ["id", "username", "role", "age", "goal",
                "sport_type", "location", "weight", "height", "avatar"]


class UserSerializer(BaseUserSerializer):
    """Расширенный сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "role", "age", "goal",
                  "sport_type", "location", "weight", "height", "avatar"]


class TrainerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    social_links = serializers.DictField(
        child=serializers.URLField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = TrainerProfile
        fields = [
            "id",
            "user",
            "bio",
            "certificates",
            "rating",
            "social_links"
        ]

    def validate_social_links(self, value):
        validator = URLValidator()
        for url in value.values():
            validator(url)  # Вызовет ValidationError при ошибке
        return value


class UserShortSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списков"""
    class Meta:
        model = User
        fields = ["id", "username", "role"]


class FriendshipSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)  # Инициатор заявки
    friend = UserShortSerializer(read_only=True)  # Получатель заявки
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
        help_text="Человеко-читаемый статус заявки"
    )

    class Meta:
        model = Friendship
        fields = [
            "id",
            "user",
            "friend",
            "status",
            "status_display",
            "created_at"
        ]
        read_only_fields = ["user", "created_at"]
