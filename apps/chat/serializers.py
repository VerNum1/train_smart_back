from rest_framework import serializers
from apps.chat.models import MessageFile, Message, Chat


class MessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFile
        fields = ['file', 'file_type']


class MessageSerializer(serializers.ModelSerializer):
    files = MessageFileSerializer(many=True, read_only=True)
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'timestamp', 'is_read', 'files']


class ChatSerializer(serializers.ModelSerializer):
    partner = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'partner', 'last_message', 'created_at']

    def get_partner(self, obj):
        user = self.context['request'].user
        partner = obj.participant1 if user == obj.participant2 else obj.participant2
        return {
            'id': partner.id,
            'username': partner.username,
            'role': partner.role
        }

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        return MessageSerializer(last_msg).data if last_msg else None


class MessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['is_read']
