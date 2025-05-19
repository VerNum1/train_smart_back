from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.product.models import Product
from apps.training.models import Training, TrainingSession
from apps.user_activity.models import UserActivity
from apps.users.models import TrainerProfile, Friendship
from apps.video_call.models import VideoCall

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'role', 'age', 'gender')
    list_filter = ('role', 'gender')
    search_fields = ('username', 'email')


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'social_links')
    search_fields = ('user__username',)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'created_by')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'description')


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'training', 'completed_at', 'rating')
    search_fields = ('user__username', 'training__title')


@admin.register(VideoCall)
class VideoCallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'receiver', 'status', 'call_type', 'start_time', 'end_time')
    list_filter = ('status', 'call_type')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'location', 'duration')
    list_filter = ('action',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'popularity_score')
    list_filter = ('category', 'target_gender')
    search_fields = ('title', 'description', 'keywords')
