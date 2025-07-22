# apps/approval/urls.py
from django.urls import path
from . import views

app_name = 'approval'

urlpatterns = [
    # Web Views
    path('', views.ApprovalListView.as_view(), name='request-list'),
    path('<int:pk>/', views.ApprovalDetailView.as_view(), name='request-detail'),
    path('<int:pk>/<str:action>/', views.ApprovalActionView.as_view(), name='request-action'),
    
    # API Endpoints
    path('api/requests/', views.ApprovalRequestAPI.as_view(), name='api-request-list'),
    path('api/requests/<int:pk>/<str:action>/', views.ApprovalActionAPI.as_view(), name='api-request-action'),
]