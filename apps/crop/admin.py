#apps\crop\admin.py
from django.contrib import admin
from .models import CropType, Crop, CropStage


@admin.register(CropType)
class CropTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'growth_duration', 'optimal_temperature_min', 'optimal_temperature_max', 'optimal_ph_min', 'optimal_ph_max')
    search_fields = ('name', 'scientific_name')
    list_filter = ('growth_duration',)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'crop_type', 'farm', 'status', 'planting_date', 'harvest_date', 'area', 'expected_yield', 'actual_yield')
    list_filter = ('status', 'planting_date', 'harvest_date')
    search_fields = ('crop_type__name', 'farm__name')
    autocomplete_fields = ('farm', 'crop_type')


@admin.register(CropStage)
class CropStageAdmin(admin.ModelAdmin):
    list_display = ('crop', 'name', 'start_date', 'end_date', 'completed')
    list_filter = ('completed', 'start_date')
    search_fields = ('crop__crop_type__name', 'name')
