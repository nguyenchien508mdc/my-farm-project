from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from pydantic import ValidationError
from apps.farm.models import FarmDocument, FarmMembership
from apps.farm.schemas.document_schema import FarmDocumentCreateUpdateSchema
from apps.farm.mappers.document_mapper import document_to_schema

from apps.farm.services.document_service import DocumentService


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


def normalize_document_data(data):
    normalized = {}
    for k, v in data.items():
        if isinstance(v, list):
            v = v[0]

        if k in ["issue_date", "expiry_date"] and (v == "" or v is None):
            v = None

        if k == "farm_id":
            try:
                v = int(v)
            except ValueError:
                pass

        normalized[k] = v
    return normalized


class FarmDocumentViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsFarmAdminManagerOrAsst]
    service = DocumentService()

    def list(self, request):
        documents = FarmDocument.objects.select_related('farm').all()
        data = [document_to_schema(d).dict() for d in documents]
        return Response(data)

    def create(self, request):
        try:
            data = normalize_document_data(request.data.copy())
            file = request.FILES.get("file")
            schema_in = FarmDocumentCreateUpdateSchema(**data)

            # Tạo document qua service
            document = FarmDocument(**schema_in.dict())
            if file:
                document.file = file
            document.save()

            return Response(document_to_schema(document).dict(), status=201)

        except ValidationError as e:
            return Response(e.errors(), status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def retrieve(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)
        return Response(document_to_schema(document).dict())

    def update(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)

        try:
            data = normalize_document_data(request.data.copy())
            file = request.FILES.get("file")

            schema_in = FarmDocumentCreateUpdateSchema(**{k: v for k, v in data.items() if k != "file"})
            for key, value in schema_in.dict().items():
                setattr(document, key, value)

            if file:
                document.file = file

            document.save()
            return Response(document_to_schema(document).dict())

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

        return Response(document_to_schema(document).dict())

    def destroy(self, request, pk=None):
        document = get_object_or_404(FarmDocument, pk=pk)
        self.check_object_permissions(request, document)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FarmDocumentByFarmView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farm_id):
        documents = FarmDocument.objects.select_related('farm').filter(farm_id=farm_id)
        data = [document_to_schema(d).dict() for d in documents]
        return Response(data)
