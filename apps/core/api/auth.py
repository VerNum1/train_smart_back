from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "Пользователь создан"}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Авторизация с получением JWT-токена"""
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetRequestView(generics.GenericAPIView):
    """Инициирование сброса пароля"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"https://example.com/reset-password/{uid}/{token}/"

            send_mail(
                'Сброс пароля',
                f'Перейдите по ссылке: {reset_url}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"status": "Письмо отправлено"})
        return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(generics.GenericAPIView):
    """Подтверждение сброса пароля"""
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(request.data.get('new_password'))
                user.save()
                return Response({"status": "Пароль изменен"})

            return Response({"error": "Неверный токен"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
