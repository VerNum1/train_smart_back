from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User, Friendship
from apps.users.serializers import UserProfileSerializer, FriendshipSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class FriendshipViewSet(viewsets.ModelViewSet):
    """Управление друзьями"""
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Принять заявку в друзья"""
        friendship = self.get_object()
        friendship.status = 'ACCEPTED'
        friendship.save()
        return Response({"status": "Заявка принята"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Отклонить заявку"""
        friendship = self.get_object()
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
