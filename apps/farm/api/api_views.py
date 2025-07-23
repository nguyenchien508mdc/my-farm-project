from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from apps.farm.models import Farm, FarmMembership, FarmDocument
from apps.farm.schemas.farm_schema import FarmCreateUpdateSchema, FarmOutSchema, FarmPartialUpdateSchema
from apps.farm.schemas.membership_schema import FarmMembershipCreateUpdateSchema, FarmMembershipOutSchema
from apps.farm.schemas.document_schema import FarmDocumentCreateUpdateSchema, FarmDocumentOutSchema

from apps.farm.mappers.farm_mapper import farm_to_schema, create_farm_from_schema, update_farm_from_schema
from apps.farm.mappers.membership_mapper import membership_to_schema, create_membership_from_schema, update_membership_from_schema
from apps.farm.mappers.document_mapper import document_to_schema, create_document_from_schema, update_document_from_schema

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
    """
    Chuẩn hóa dữ liệu Farm từ request.data trước khi parse Pydantic:
    - Nếu field là list, lấy phần tử đầu
    - Ép kiểu 'area' thành float
    - Ép kiểu 'is_active' thành bool
    """
    normalized = {}
    for k, v in data.items():
        # Nếu là list thì lấy phần tử đầu
        if isinstance(v, list):
            v = v[0]
        normalized[k] = v

    # Ép kiểu is_active
    if "is_active" in normalized:
        val = str(normalized["is_active"]).lower()
        normalized["is_active"] = val in ["true", "1"]

    # Ép kiểu area
    if "area" in normalized:
        try:
            normalized["area"] = float(normalized["area"])
        except (ValueError, TypeError):
            # Nếu không convert được thì giữ nguyên để schema bắt lỗi
            pass

    return normalized


class FarmViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]

    def list(self, request):
        farms = Farm.objects.all()
        return Response([farm_to_schema(f).dict() for f in farms])

    def create(self, request):
        try:
            data = request.data.copy()
            logo_file = data.get("logo")

            farm_dict = normalize_farm_data(data)
            farm_in = FarmCreateUpdateSchema(**{k: v for k, v in farm_dict.items() if k != "logo"})
            farm = create_farm_from_schema(farm_in)

            if logo_file:
                farm.logo = logo_file

            farm.save()
            return Response(farm_to_schema(farm).dict(), status=201)

        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def update(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        self.check_object_permissions(request, farm)

        try:
            data = request.data.copy()
            farm_dict = normalize_farm_data(data)
            farm_in = FarmCreateUpdateSchema(**farm_dict)

            farm = update_farm_from_schema(farm, farm_in)
            farm.save()
            return Response(farm_to_schema(farm).dict())

        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def partial_update(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        self.check_object_permissions(request, farm)

        try:
            data = request.data.copy()
            logo_file = data.get("logo")

            farm_dict = normalize_farm_data({k: v for k, v in data.items() if k != "logo"})
            farm_in = FarmPartialUpdateSchema(**farm_dict)
            update_data = farm_in.dict(exclude_unset=True)

            for key, value in update_data.items():
                setattr(farm, key, value)

            if logo_file:
                farm.logo = logo_file

            farm.save()
            return Response(farm_to_schema(farm).dict())

        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def retrieve(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        self.check_object_permissions(request, farm)
        return Response(farm_to_schema(farm).dict())

    def destroy(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        self.check_object_permissions(request, farm)
        farm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FarmMembershipViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]

    def list(self, request):
        memberships = FarmMembership.objects.select_related('user', 'farm').all()
        data = [membership_to_schema(m).dict() for m in memberships]
        return Response(data)

    def create(self, request):
        try:
            membership_in = FarmMembershipCreateUpdateSchema(**request.data)
        except ValidationError as e:
            return Response(e.errors(), status=400)

        # Check existing membership
        if FarmMembership.objects.filter(
            farm_id=membership_in.farm_id, user_id=membership_in.user_id
        ).exists():
            return Response({"detail": "Người dùng đã là thành viên của nông trại này"}, status=400)

        membership = create_membership_from_schema(membership_in)
        membership.save()
        membership_out = membership_to_schema(membership)
        return Response(membership_out.dict(), status=201)

    def retrieve(self, request, pk=None):
        membership = get_object_or_404(FarmMembership, pk=pk)
        self.check_object_permissions(request, membership)
        membership_out = membership_to_schema(membership)
        return Response(membership_out.dict())

    def update(self, request, pk=None):
        membership = get_object_or_404(FarmMembership, pk=pk)
        self.check_object_permissions(request, membership)

        try:
            membership_in = FarmMembershipCreateUpdateSchema(**request.data)
        except ValidationError as e:
            return Response(e.errors(), status=400)

        # Check duplication if changing farm or user
        if (membership.farm_id != membership_in.farm_id or membership.user_id != membership_in.user_id) and \
           FarmMembership.objects.filter(farm_id=membership_in.farm_id, user_id=membership_in.user_id).exclude(pk=pk).exists():
            return Response({"detail": "Người dùng đã là thành viên của nông trại này"}, status=400)

        membership = update_membership_from_schema(membership, membership_in)
        membership.save()

        membership_out = membership_to_schema(membership)
        return Response(membership_out.dict())

    def partial_update(self, request, pk=None):
        membership = get_object_or_404(FarmMembership, pk=pk)
        self.check_object_permissions(request, membership)

        for key, value in request.data.items():
            setattr(membership, key, value)
        membership.save()

        membership_out = membership_to_schema(membership)
        return Response(membership_out.dict())

    def destroy(self, request, pk=None):
        membership = get_object_or_404(FarmMembership, pk=pk)
        self.check_object_permissions(request, membership)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def normalize_document_data(data):
    normalized = {}
    for k, v in data.items():
        # Nếu là list (đến từ QueryDict), lấy phần tử đầu tiên
        if isinstance(v, list):
            v = v[0]

        # Nếu là ngày rỗng, chuyển thành None
        if k in ["issue_date", "expiry_date"] and (v == "" or v is None):
            v = None

        # Ép farm_id thành int nếu cần
        if k == "farm_id":
            try:
                v = int(v)
            except ValueError:
                pass

        normalized[k] = v
    return normalized

class FarmDocumentViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]

    def list(self, request):
        documents = FarmDocument.objects.select_related('farm').all()
        data = [document_to_schema(d).dict() for d in documents]
        return Response(data)

    def create(self, request):
        try:
            data = normalize_document_data(request.data)
            doc_in = FarmDocumentCreateUpdateSchema(**data)
            document = create_document_from_schema(doc_in)
            document.save()
            doc_out = document_to_schema(document)
            return Response(doc_out.dict(), status=201)

        except ValidationError as e:
            return Response(e.errors(), status=400)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)


    def retrieve(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)
        doc_out = document_to_schema(document)
        return Response(doc_out.dict())

    def update(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)

        try:
            # Ép kiểu dữ liệu file nếu có
            data = request.data.copy()
            file = data.get("file")  # <-- Lấy file mới (nếu có)

            doc_in = FarmDocumentCreateUpdateSchema(**{k: v for k, v in data.items() if k != "file"})

            document = update_document_from_schema(document, doc_in)

            if file:
                document.file = file  # Chỉ cập nhật nếu có file mới

            document.save()
            doc_out = document_to_schema(document)
            return Response(doc_out.dict())

        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)


    def partial_update(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)

        for key, value in request.data.items():
            setattr(document, key, value)
        document.save()

        doc_out = document_to_schema(document)
        return Response(doc_out.dict())

    def destroy(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FarmMembershipByFarmView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farm_id):
        memberships = FarmMembership.objects.select_related('user', 'farm').filter(farm_id=farm_id)
        data = [membership_to_schema(m).dict() for m in memberships]
        return Response(data)


class FarmDocumentByFarmView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farm_id):
        documents = FarmDocument.objects.select_related('farm').filter(farm_id=farm_id)
        data = [document_to_schema(d).dict() for d in documents]
        return Response(data)


class UserFarmListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        farms = Farm.objects.filter(farmmembership__user__id=user_id).distinct()
        data = [farm_to_schema(f).dict() for f in farms]
        return Response({"farms": data}, status=status.HTTP_200_OK)
