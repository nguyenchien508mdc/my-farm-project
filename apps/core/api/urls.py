# apps/core/api_urls.py

from django.urls import path
from . import views, api_views

urlpatterns = [
    # ✅ API người dùng
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('me/', api_views.MeAPIView.as_view(), name='api_me'),
    path('password-change/', api_views.ChangePasswordAPIView.as_view(), name='api_password_change'),
    path('password-reset/', api_views.PasswordResetAPIView.as_view(), name='api_password_reset'),
    path('password-reset-confirm/', api_views.PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
    path('users/', api_views.UserListAPIView.as_view(), name='user-list'),
    path('free-users/<int:farm_id>/', api_views.FreeUsersAPIView.as_view(), name='free-users'),
    path('token/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', api_views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', api_views.logout_view, name='logout'),
]
