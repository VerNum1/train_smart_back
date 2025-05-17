from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.chat.models import MessageFile, Message, Chat
from apps.chat.serializers import MessageReadSerializer, ChatSerializer


class MessageFileUploadView(generics.CreateAPIView):
    queryset = MessageFile.objects.all()
    parser_classes = [MultiPartParser]

    def create(self, request, message_id):
        message = Message.objects.get(id=message_id)
        files = request.FILES.getlist('files')

        for file in files:
            file_type = file.content_type.split('/')[0]
            MessageFile.objects.create(
                message=message,
                file=file,
                file_type=file_type
            )

        return Response(status=status.HTTP_201_CREATED)


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(
            Q(participant1=user) |
            Q(participant2=user)
        ).prefetch_related('messages').order_by('-last_message')

    def get_serializer_context(self):
        return {'request': self.request}


class MarkMessageReadView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def perform_update(self, serializer):
        message = self.get_object()
        if self.request.user not in [message.chat.participant1, message.chat.participant2]:
            raise PermissionDenied("Вы не участник этого чата")
        serializer.save(is_read=True)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
