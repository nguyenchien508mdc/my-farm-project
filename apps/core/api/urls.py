# apps/core/api_urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ✅ API người dùng
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('me/', views.MeAPIView.as_view(), name='api_me'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('password-reset/', views.PasswordResetAPIView.as_view(), name='api_password_reset'),
    path('password-reset-confirm/', views.PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('free-users/<int:farm_id>/', views.FreeUsersAPIView.as_view(), name='free-users'),
]
