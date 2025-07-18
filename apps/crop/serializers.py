#apps\crop\serializers.py
from rest_framework import serializers
from .models import CropType, Crop, CropStage

class CropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropType
        fields = [
            'id', 'name', 'scientific_name', 'description',
            'growth_duration', 'optimal_temperature_min', 'optimal_temperature_max',
            'optimal_ph_min', 'optimal_ph_max', 'image'
        ]


class CropStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropStage
        fields = [
            'id', 'crop', 'name', 'start_date', 'end_date',
            'description', 'completed'
        ]


class CropSerializer(serializers.ModelSerializer):
    crop_type = CropTypeSerializer(read_only=True)
    crop_type_id = serializers.PrimaryKeyRelatedField(
        queryset=CropType.objects.all(),
        write_only=True,
        source='crop_type'
    )

    stages = CropStageSerializer(many=True, read_only=True)

    class Meta:
        model = Crop
        fields = [
            'id', 'farm', 'crop_type', 'crop_type_id', 'variety', 'status',
            'planting_date', 'harvest_date', 'area', 'expected_yield',
            'actual_yield', 'notes', 'stages'
        ]
