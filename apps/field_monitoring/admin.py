from django.contrib import admin
from .models import SoilMeasurement, WeatherRecord

@admin.register(SoilMeasurement)
class SoilMeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'farm', 'location', 'ph', 'organic_matter', 'measurement_date', 'thumbnail'
    )
    list_filter = ('farm', 'measurement_date')
    search_fields = ('location', 'farm__name')
    autocomplete_fields = ['farm']
    date_hierarchy = 'measurement_date'
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" height="80" style="object-fit:cover;border-radius:4px;" />'
        return "No image"
    thumbnail.short_description = "Hình ảnh"
    thumbnail.allow_tags = True  # For Django <3.0
    thumbnail.admin_order_field = 'image'

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = (
        'farm', 'record_date', 'temperature', 'humidity', 'rainfall',
        'wind_speed', 'weather_condition', 'sunshine_hours'
    )
    list_filter = ('record_date', 'weather_condition')
    search_fields = ('farm__name', 'weather_condition')
    autocomplete_fields = ['farm']
    date_hierarchy = 'record_date'
