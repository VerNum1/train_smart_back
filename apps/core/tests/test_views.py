from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from rest_framework import status

from apps.users.models import Friendship


# --- RegisterView ---
@pytest.mark.django_db
def test_register_user():
    url = reverse('register')
    data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepass123"
    }
    response = APIClient().post(url, data)
    assert response.status_code == 201
    assert response.data["status"] == "Пользователь создан"

# --- Token (CustomTokenObtainPairView) ---
@pytest.mark.django_db
def test_obtain_token(user):
    url = reverse('token_obtain_pair')
    data = {"email": user.email, "password": "password123"}
    response = APIClient().post(url, data)
    assert "access" in response.data
    assert response.status_code == 200

# --- PasswordResetRequestView ---
@pytest.mark.django_db
def test_password_reset_request(user):
    url = reverse('password_reset_request')
    response = APIClient().post(url, {"email": user.email})
    assert response.status_code == 200

@pytest.mark.django_db
def test_password_reset_confirm(user):
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.contrib.auth.tokens import default_token_generator

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = reverse('password_reset_confirm', args=[uid, token])
    response = APIClient().post(url, {"new_password": "newpassword123"})
    assert response.status_code == 200

# --- UserProfileView ---
@pytest.mark.django_db
def test_get_user_profile(auth_client):
    url = reverse('user-profile')
    response = auth_client.get(url)
    assert response.status_code == 200

# --- TrainingViewSet ---
@pytest.mark.django_db
def test_create_training(auth_client):
    url = reverse('training-list')
    data = {
        "title": "Test Training",
        "description": "Test Desc",
        "duration": 45
    }
    response = auth_client.post(url, data)
    assert response.status_code == 201

# --- VideoCallViewSet ---
@pytest.mark.django_db
def test_start_video_call(auth_client, user):
    url = reverse('videocall-start-call')
    response = auth_client.post(url, {"receiver_id": user.id})
    assert response.status_code == 200

# --- UserActivityView ---
@pytest.mark.django_db
def test_user_activity_list(auth_client):
    url = reverse('user-activity')
    response = auth_client.get(url)
    assert response.status_code == 200

# --- NotificationListView ---
@pytest.mark.django_db
def test_notifications_list(auth_client):
    url = reverse('notifications')
    response = auth_client.get(url)
    assert response.status_code == 200

# --- TrainerProfileViewSet ---
@pytest.mark.django_db
def test_trainer_profile_list():
    url = reverse('trainerprofile-list')
    response = APIClient().get(url)
    assert response.status_code == 200

# --- FriendshipViewSet ---
@pytest.mark.django_db
def test_friendship_accept(auth_client, user):
    friendship = Friendship.objects.create(requester=user, receiver=auth_client.handler._force_user)
    url = reverse('friendship-accept', args=[friendship.id])
    response = auth_client.post(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_friendship_reject(auth_client, user):
    friendship = Friendship.objects.create(requester=user, receiver=auth_client.handler._force_user)
    url = reverse('friendship-reject', args=[friendship.id])
    response = auth_client.post(url)
    assert response.status_code == 204

# --- ProductRecommendationAPI ---
@pytest.mark.django_db
def test_product_recommendations(auth_client, mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"recommendations": []}
    mock_response.status_code = 200

    mocker.patch("requests.post", return_value=mock_response)

    url = reverse('product-recommendations')
    response = auth_client.get(url)
    assert response.status_code in [200, 206]
