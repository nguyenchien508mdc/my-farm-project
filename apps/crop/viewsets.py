# apps/crop/viewsets.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Crop
from .services import CropService
from .serializers import CropSerializer
from rest_framework.decorators import action

class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            crop = CropService.create_crop(
                farm_id=serializer.validated_data['farm'],
                crop_type_id=serializer.validated_data['crop_type_id'],
                **serializer.validated_data
            )
            return Response(
                self.get_serializer(crop).data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        crop = self.get_object()
        new_status = request.data.get('status')
        
        try:
            crop = CropService.update_crop_status(crop.id, new_status)
            return Response(
                self.get_serializer(crop).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )