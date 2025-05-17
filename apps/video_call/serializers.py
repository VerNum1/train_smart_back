from rest_framework import serializers

from apps.video_call.models import VideoCall


class VideoCallSerializer(serializers.ModelSerializer):
    caller = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    receiver = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = VideoCall
        fields = [
            "id",
            "caller",
            "receiver",
            "start_time",
            "end_time",
            "status"
        ]
        read_only_fields = ["start_time", "end_time", "status"]