#apps\farm\api\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views, farm_api, document_api, membership_api

# Tạo router và đăng ký các ViewSet
router = DefaultRouter()
router.register(r'farms', farm_api.FarmViewSet, basename='farm')
router.register(r'memberships', membership_api.FarmMembershipViewSet, basename='farm_membership')
router.register(r'documents', document_api.FarmDocumentViewSet, basename='farm_document')

# Tập hợp tất cả các route đã đăng ký
urlpatterns = [
    path('', include(router.urls)),
    path('farms/<int:farm_id>/memberships/', membership_api.FarmMembershipByFarmView.as_view(), name='farm-members'),
    path('farms/<int:farm_id>/documents/', document_api.FarmDocumentByFarmView.as_view(), name='farm-documents'),
    path('users/<int:user_id>/all-farms/', farm_api.UserFarmListAPIView.as_view(), name='user-farm-list'),
]
