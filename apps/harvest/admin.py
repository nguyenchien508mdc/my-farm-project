from django.contrib import admin
from .models import Harvest

@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ('id', 'farm', 'crop', 'harvest_date', 'quantity', 'unit', 'quality', 'storage_location')
    list_filter = ('farm', 'quality', 'harvest_date')
    search_fields = ('farm__name', 'crop__crop_type__name')
    autocomplete_fields = ['farm', 'crop']
    date_hierarchy = 'harvest_date'
    readonly_fields = ('id',)

    fieldsets = (
        (None, {
            'fields': ('id', 'farm', 'crop', 'harvest_date', 'quantity', 'unit', 'quality')
        }),
        ('Thông tin bổ sung', {
            'classes': ('collapse',),
            'fields': ('storage_location', 'notes'),
        }),
    )
