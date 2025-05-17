from django_filters.rest_framework import DjangoFilterBackend

from apps.core.pagination import CustomPagination
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from apps.core.filters import TrainingFilter
from apps.training.models import Training
from apps.training.serializers import TrainingSerializer


class TrainingViewSet(viewsets.ModelViewSet):
    """CRUD для тренировок"""
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TrainingFilter
    search_fields = ['title', 'description']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
