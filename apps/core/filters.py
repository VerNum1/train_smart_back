import django_filters

from apps.product.models import Product
from apps.training.models import Training
from apps.users.models import TrainerProfile


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'target_gender']


class TrainingFilter(django_filters.FilterSet):
    min_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    max_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    sport_type = django_filters.CharFilter(field_name='sport_type')

    class Meta:
        model = Training
        fields = ['category', 'sport_type']
        search_fields = ['title', 'description']


class TrainerFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(field_name='user__age', lookup_expr='gte')
    max_age = django_filters.NumberFilter(field_name='user__age', lookup_expr='lte')
    gender = django_filters.CharFilter(field_name='user__gender')
    sport_type = django_filters.CharFilter(field_name='sport_type')

    class Meta:
        model = TrainerProfile
        fields = []


class ProgramFilter(django_filters.FilterSet):
    difficulty = django_filters.ChoiceFilter(choices=Training.DIFFICULTY_CHOICES)
    sport_type = django_filters.CharFilter(field_name='sport_type')

    class Meta:
        model = Training
        fields = ['category', 'difficulty']


