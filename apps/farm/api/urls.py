#apps\farm\api\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Tạo router và đăng ký các ViewSet
router = DefaultRouter()
router.register(r'farms', api_views.FarmViewSet, basename='farm')
router.register(r'memberships', api_views.FarmMembershipViewSet, basename='farm_membership')
router.register(r'documents', api_views.FarmDocumentViewSet, basename='farm_document')

# Tập hợp tất cả các route đã đăng ký
urlpatterns = [
    path('', include(router.urls)),
    path('farms/<int:farm_id>/memberships/', api_views.FarmMembershipByFarmView.as_view(), name='farm-members'),
    path('farms/<int:farm_id>/documents/', api_views.FarmDocumentByFarmView.as_view(), name='farm-documents'),
    path('users/<int:user_id>/all-farms/', api_views.UserFarmListAPIView.as_view(), name='user-farm-list'),
]
