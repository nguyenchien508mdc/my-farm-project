#apps\crop\views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from .services import CropService, CropTypeService
from .models import Crop
from .serializers import CropSerializer, CropTypeSerializer


class CropListCreateAPIView(APIView):
    def get(self, request):
        crops = Crop.objects.all()
        serializer = CropSerializer(crops, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CropSerializer(data=request.data)
        if serializer.is_valid():
            try:
                crop = CropService.create_crop(
                    farm_id=request.data.get('farm'),
                    crop_type_id=request.data.get('crop_type_id'),
                    **serializer.validated_data
                )
                return Response(CropSerializer(crop).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CropDetailAPIView(APIView):
    def get_object(self, pk):
        return Crop.objects.get(pk=pk)

    def get(self, request, pk):
        crop = self.get_object(pk)
        serializer = CropSerializer(crop)
        return Response(serializer.data)

    def put(self, request, pk):
        crop = self.get_object(pk)
        serializer = CropSerializer(crop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        crop = self.get_object(pk)
        crop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CropHealthAPIView(APIView):
    def get(self, request, pk):
        try:
            result = CropService.get_crop_health(pk)
            return Response(result)
        except Crop.DoesNotExist:
            return Response({"error": "Crop not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CropTypeListCreateAPIView(APIView):
    def get(self, request):
        crop_types = CropTypeService.recommend_crops(farm_id=request.query_params.get('farm'))
        serializer = CropTypeSerializer(crop_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CropTypeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                crop_type = CropTypeService.create_crop_type(
                    name=serializer.validated_data['name'],
                    growth_duration=serializer.validated_data['growth_duration'],
                    temp_min=serializer.validated_data['optimal_temperature_min'],
                    temp_max=serializer.validated_data['optimal_temperature_max'],
                    ph_min=serializer.validated_data['optimal_ph_min'],
                    ph_max=serializer.validated_data['optimal_ph_max'],
                    **serializer.validated_data
                )
                return Response(CropTypeSerializer(crop_type).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
