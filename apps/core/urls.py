# apps/core/urls.py

from django.urls import path
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='blank_app.html'), name='home'),

    # Public layout (dành cho người chưa đăng nhập)
    path('login/', TemplateView.as_view(template_name='blank_public.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='blank_public.html'), name='register'),
    path('password-reset/', TemplateView.as_view(template_name='blank_public.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', TemplateView.as_view(template_name='blank_public.html'), name='password_reset_confirm'),

    # App layout (dành cho người đã đăng nhập)
    path('profile/', TemplateView.as_view(template_name='blank_app.html'), name='profile'),
    path('profile-update/', TemplateView.as_view(template_name='blank_app.html'), name='profile_update'),
    path('password-change/', TemplateView.as_view(template_name='blank_app.html'), name='password_change'),
]