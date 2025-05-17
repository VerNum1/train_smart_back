"""
URL configuration for train_smart_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.core.api.auth import RegisterView, CustomTokenObtainPairView, PasswordResetRequestView, \
    PasswordResetConfirmView


urlpatterns = [
    path('/', include('apps.chat.urls')),
    path('/', include('apps.training.urls')),
    path('/', include('apps.users.urls')),
    path('/', include('apps.notification.urls')),
    path('/', include('apps.product.urls')),
    path('/', include('apps.user_activity.urls')),
    path('/', include('apps.video_call.urls')),

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/', admin.site.urls),
]
