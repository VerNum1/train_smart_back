from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import requests
import json

from config import settings
from .models import Product
from .serializers import ProductSerializer
from ..user_activity.models import UserActivity

User = get_user_model()


class ProductRecommendationAPI(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Собираем данные пользователя
        user_data = {
            "gender": User.gender,
            "age": User.age,
            "sport_type": User.sport_type,
            "goal": User.goal,
            "location": User.location,
            "weight": User.weight,
            "height": User.height,
        }

        # Собираем последние активности
        activities = UserActivity.objects.filter(user=user).order_by('-timestamp')[:10]
        activity_log = [
            {
                "action": a.action,
                "product": a.product.title if a.product else None,
                "timestamp": a.timestamp.isoformat()
            }
            for a in activities
        ]

        # Формируем промт для GigaChat
        prompt = f"""
        Пользователь ({user_data}) с историей активностей: {activity_log}.
        Рекомендуй подходящие спортивные товары из доступных категорий: {Product.CATEGORY_CHOICES}.
        Учитывай пол, возраст, цели и историю взаимодействий.
        Верни только JSON массив с ID товаров в порядке релевантности.
        """

        try:
            # Запрос к GigaChat API
            response = requests.post(
                'https://gigachat/api/v1/recommend',
                headers={
                    'Authorization': f'Bearer {settings.GIGACHAT_API_KEY}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "prompt": prompt,
                    "max_tokens": 1000,
                    "temperature": 0.7
                })
            )

            # Парсинг ответа
            recommended_ids = response.json().get('recommendations', [])
            recommended_products = Product.objects.filter(id__in=recommended_ids)

            # Сериализация результатов
            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data)

        except Exception as e:
            # Fallback: топ товаров по популярности
            fallback_products = Product.objects.order_by('-popularity_score')[:12]
            serializer = ProductSerializer(fallback_products, many=True)
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)