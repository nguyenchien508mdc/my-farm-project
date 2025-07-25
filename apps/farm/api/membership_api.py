import asyncio
from rest_framework.viewsets import ViewSet 
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from pydantic import ValidationError

from apps.farm.models import FarmMembership
from apps.farm.services.membership_service import FarmMembershipService
from apps.farm.schemas.membership_schema import FarmMembershipCreateUpdateSchema
from apps.farm.mappers.membership_mapper import membership_to_schema


class IsFarmAdminManagerOrAsst(BasePermission):
    ALLOWED_ROLES = ['admin', 'manager', 'assistant_manager']

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        farm = getattr(obj, 'farm', None) or obj

        try:
            membership = FarmMembership.objects.get(farm=farm, user=request.user, is_active=True)
        except FarmMembership.DoesNotExist:
            return False

        if request.method in SAFE_METHODS:
            return True

        return membership.role in self.ALLOWED_ROLES


class FarmMembershipViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]
    service = FarmMembershipService()

    def list(self, request):
        memberships = asyncio.run(self.service.list_memberships())
        data = [membership_to_schema(m).dict() for m in memberships]
        return Response(data)

    def retrieve(self, request, pk=None):
        membership = asyncio.run(self.service.get_membership(int(pk)))
        if not membership:
            return Response({"detail": "Not found"}, status=404)
        self.check_object_permissions(request, membership)
        return Response(membership_to_schema(membership).dict())

    def create(self, request):
        try:
            schema = FarmMembershipCreateUpdateSchema(**request.data)
        except ValidationError as e:
            return Response(e.errors(), status=400)

        existing = asyncio.run(self.service.repo.get_by_user_farm(schema.user_id, schema.farm_id))
        if existing:
            return Response({"detail": "Người dùng đã là thành viên của nông trại này"}, status=400)

        try:
            membership = asyncio.run(self.service.create_membership(schema))
            return Response(membership_to_schema(membership).dict(), status=201)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def update(self, request, pk=None):
        membership = asyncio.run(self.service.get_membership(int(pk)))
        if not membership:
            return Response({"detail": "Not found"}, status=404)
        self.check_object_permissions(request, membership)

        try:
            schema = FarmMembershipCreateUpdateSchema(**request.data)
        except ValidationError as e:
            return Response(e.errors(), status=400)

        try:
            updated = asyncio.run(self.service.update_membership(int(pk), schema))
            return Response(membership_to_schema(updated).dict())
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def partial_update(self, request, pk=None):
        membership = asyncio.run(self.service.get_membership(int(pk)))
        if not membership:
            return Response({"detail": "Not found"}, status=404)
        self.check_object_permissions(request, membership)

        for key, value in request.data.items():
            setattr(membership, key, value)
        membership.save()

        return Response(membership_to_schema(membership).dict())

    def destroy(self, request, pk=None):
        membership = asyncio.run(self.service.get_membership(int(pk)))
        if not membership:
            return Response({"detail": "Not found"}, status=404)
        self.check_object_permissions(request, membership)
        asyncio.run(self.service.delete_membership(int(pk)))
        return Response(status=status.HTTP_204_NO_CONTENT)


class FarmMembershipByFarmView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farm_id):
        service = FarmMembershipService()
        all_members = asyncio.run(service.list_memberships())
        members = [m for m in all_members if m.farm_id == int(farm_id)]
        data = [membership_to_schema(m).dict() for m in members]
        return Response(data)
