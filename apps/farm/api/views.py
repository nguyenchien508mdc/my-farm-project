# apps/farm/api/views.py
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    FarmSerializer, FarmCreateUpdateSerializer,
    FarmMembershipSerializer, FarmMembershipCreateUpdateSerializer,
    FarmDocumentSerializer, FarmDocumentCreateUpdateSerializer,
    SimpleFarmSerializer,
)
from ..models import Farm, FarmMembership, FarmDocument

# Permission class: 
# Superuser toàn quyền, farm member role admin/manager/assistant_manager được chỉnh sửa/xóa
class IsFarmAdminManagerOrAsst(BasePermission):
    ALLOWED_ROLES = ['admin', 'manager', 'assistant_manager']

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Lấy farm liên quan
        farm = getattr(obj, 'farm', None) or obj

        try:
            membership = FarmMembership.objects.get(farm=farm, user=request.user, is_active=True)
        except FarmMembership.DoesNotExist:
            return False

        if request.method in SAFE_METHODS:
            # Các member farm đều được đọc
            return True

        # Chỉ admin/manager/assistant_manager được phép sửa, xóa
        return membership.role in self.ALLOWED_ROLES


# ViewSet Farm
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FarmCreateUpdateSerializer
        return FarmSerializer


# ViewSet Thành viên farm
class FarmMembershipViewSet(viewsets.ModelViewSet):
    queryset = FarmMembership.objects.select_related('user', 'farm').all()
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FarmMembershipCreateUpdateSerializer
        return FarmMembershipSerializer


# ViewSet Tài liệu farm
class FarmDocumentViewSet(viewsets.ModelViewSet):
    queryset = FarmDocument.objects.select_related('farm').all()
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FarmDocumentCreateUpdateSerializer
        return FarmDocumentSerializer


# Lấy danh sách thành viên theo farm_id (chỉ cần đăng nhập)
class FarmMembershipByFarmView(generics.ListAPIView):
    serializer_class = FarmMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        farm_id = self.kwargs.get('farm_id')
        return FarmMembership.objects.select_related('user', 'farm').filter(farm_id=farm_id)


# Lấy danh sách tài liệu theo farm_id (chỉ cần đăng nhập)
class FarmDocumentByFarmView(generics.ListAPIView):
    serializer_class = FarmDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        farm_id = self.kwargs.get('farm_id')
        return FarmDocument.objects.select_related('farm').filter(farm_id=farm_id)
    
class UserFarmListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        farms = Farm.objects.filter(farmmembership__user__id=user_id).distinct()
        serializer = SimpleFarmSerializer(farms, many=True)
        return Response({"farms": serializer.data}, status=status.HTTP_200_OK)
