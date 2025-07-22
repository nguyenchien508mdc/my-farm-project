#apps\farm\api\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Tạo router và đăng ký các ViewSet
router = DefaultRouter()
router.register(r'farms', views.FarmViewSet, basename='farm')
router.register(r'memberships', views.FarmMembershipViewSet, basename='farm_membership')
router.register(r'documents', views.FarmDocumentViewSet, basename='farm_document')

# Tập hợp tất cả các route đã đăng ký
urlpatterns = [
    path('', include(router.urls)),
    path('farms/<int:farm_id>/memberships/', views.FarmMembershipByFarmView.as_view(), name='farm-members'),
    path('farms/<int:farm_id>/documents/', views.FarmDocumentByFarmView.as_view(), name='farm-documents'),
    path('users/<int:user_id>/all-farms/', views.UserFarmListAPIView.as_view(), name='user-farm-list'),
]
