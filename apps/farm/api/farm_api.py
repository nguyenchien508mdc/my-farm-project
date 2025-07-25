from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from rest_framework.views import APIView

from apps.farm.services.farm_service import FarmService
from apps.farm.models import Farm, FarmMembership
from apps.farm.mappers.farm_mapper import farm_to_schema
from apps.farm.schemas.farm_schema import FarmPartialUpdateSchema
from pydantic import ValidationError


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


def normalize_farm_data(data):
    normalized = {}
    for k, v in data.items():
        if isinstance(v, list):
            v = v[0]
        normalized[k] = v

    if "is_active" in normalized:
        val = str(normalized["is_active"]).lower()
        normalized["is_active"] = val in ["true", "1"]

    if "area" in normalized:
        try:
            normalized["area"] = float(normalized["area"])
        except (ValueError, TypeError):
            pass

    return normalized

import os
from django.conf import settings
from django.core.files.storage import default_storage

class FarmViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]
    service = FarmService()

    def list(self, request):
        farms = async_to_sync(self.service.list_farms)()
        data = [farm_to_schema(f).dict() for f in farms]
        return Response(data)

    def create(self, request):
        data = request.data.copy()
        logo_file = data.pop("logo", None)

        if isinstance(logo_file, list):
            logo_file = logo_file[0] if logo_file else None

        farm_dict = normalize_farm_data(data)

        try:
            farm = async_to_sync(self.service.create_farm)(farm_dict)

            if logo_file:
                farm.logo = logo_file  
                async_to_sync(farm.asave)()

            return Response(farm_to_schema(farm).dict(), status=201)

        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            print("CREATE ERROR:", str(e))
            return Response({"detail": str(e)}, status=500)


    def retrieve(self, request, pk=None):
        try:
            farm = async_to_sync(self.service.get_farm)(pk)
            self.check_object_permissions(request, farm)
            return Response(farm_to_schema(farm).dict())
        except Exception as e:
            return Response({"detail": str(e)}, status=404)

    def update(self, request, pk=None):
        try:
            self.check_object_permissions(request, get_object_or_404(Farm, pk=pk))
            farm_dict = normalize_farm_data(request.data)
            farm = async_to_sync(self.service.update_farm)(pk, farm_dict)
            return Response(farm_to_schema(farm).dict())
        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def partial_update(self, request, pk=None):
        try:
            self.check_object_permissions(request, get_object_or_404(Farm, pk=pk))
            data = normalize_farm_data({k: v for k, v in request.data.items() if k != "logo"})
            farm_in = FarmPartialUpdateSchema(**data)
            update_data = farm_in.dict(exclude_unset=True)

            farm = async_to_sync(self.service.get_farm)(pk)
            for key, value in update_data.items():
                setattr(farm, key, value)

            logo_file = request.data.get("logo")
            if logo_file:
                farm.logo = logo_file

            farm.save()
            return Response(farm_to_schema(farm).dict())
        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def destroy(self, request, pk=None):
        try:
            self.check_object_permissions(request, get_object_or_404(Farm, pk=pk))
            async_to_sync(self.service.delete_farm)(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

class UserFarmListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        farms = Farm.objects.filter(farmmembership__user__id=user_id).distinct()
        data = [farm_to_schema(f).dict() for f in farms]
        return Response({"farms": data}, status=status.HTTP_200_OK)