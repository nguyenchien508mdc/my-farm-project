from django.contrib import admin
from .models import Task, Irrigation, Fertilization

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin cho Task: quản lý công việc trên trang admin."""

    list_display = (
        'title', 'farm', 'assigned_to', 'due_date',
        'priority', 'status', 'is_completed', 'completed_date'
    )
    list_filter = ('priority', 'status', 'due_date', 'farm')
    search_fields = (
        'title', 'description', 'assigned_to__username', 'assigned_to__email'
    )
    autocomplete_fields = ['farm', 'assigned_to']
    date_hierarchy = 'due_date'
    readonly_fields = ('completed_date',)
    
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'farm', 'assigned_to',
                'due_date', 'priority', 'status', 'completed_date'
            )
        }),
        ('Liên kết đối tượng', {
            'fields': ('related_object_type', 'related_object_id'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(boolean=True, description="Đã hoàn thành")
    def is_completed(self, obj):
        return obj.status == 'completed'


@admin.register(Irrigation)
class IrrigationAdmin(admin.ModelAdmin):
    """Admin cho Irrigation: quản lý tưới tiêu."""

    list_display = (
        'farm', 'date', 'method', 'duration', 'water_amount', 'related_crop'
    )
    list_filter = ('method', 'date', 'farm')
    search_fields = ('notes', 'related_crop__name')
    autocomplete_fields = ['farm', 'related_crop']
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': (
                'farm', 'date', 'method', 'duration',
                'water_amount', 'notes', 'related_crop'
            )
        }),
    )


@admin.register(Fertilization)
class FertilizationAdmin(admin.ModelAdmin):
    """Admin cho Fertilization: quản lý bón phân."""

    list_display = (
        'farm', 'date', 'fertilizer', 'amount', 'method', 'related_crop'
    )
    list_filter = ('date', 'farm')
    search_fields = ('notes', 'fertilizer__name', 'method')
    autocomplete_fields = ['farm', 'fertilizer', 'related_crop']
    date_hierarchy = 'date'

    fieldsets = (
        (None, {
            'fields': (
                'farm', 'date', 'fertilizer', 'amount',
                'method', 'notes', 'related_crop'
            )
        }),
    )
