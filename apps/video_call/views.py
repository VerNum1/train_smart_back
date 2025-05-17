from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.video_call.models import VideoCall
from apps.video_call.serializers import VideoCallSerializer


class VideoCallViewSet(viewsets.ModelViewSet):
    """Управление видео-звонками"""
    queryset = VideoCall.objects.all()
    serializer_class = VideoCallSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def start_call(self, request):
        """Начать звонок"""
        receiver_id = request.data.get('receiver_id')
        # Логика инициализации звонка
        return Response({"status": "Звонок начат"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def end_call(self, request, pk=None):
        """Завершить звонок"""
        call = self.get_object()
        call.status = 'ENDED'
        call.save()
        return Response({"status": "Звонок завершен"})