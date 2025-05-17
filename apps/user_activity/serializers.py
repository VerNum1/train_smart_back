from rest_framework import serializers

from apps.product.serializers import ProductSerializer
from apps.training.serializers import TrainingSerializer
from apps.user_activity.models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    training = TrainingSerializer(read_only=True)

    class Meta:
        model = UserActivity
        fields = [
            'action', 'product', 'training',
            'timestamp', 'location', 'duration'
        ]