from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Report, Dashboard

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'farm', 'report_type', 'start_date', 'end_date', 'generated_at', 'generated_by')
    list_filter = ('report_type', 'farm', 'generated_at')
    search_fields = ('title', 'farm__name')
    date_hierarchy = 'generated_at'
    ordering = ('-generated_at',)
    fieldsets = (
        (_('Thông tin chung'), {
            'fields': ('farm', 'title', 'report_type')
        }),
        (_('Thời gian'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('File báo cáo'), {
            'fields': ('file',)
        }),
        (_('Người tạo'), {
            'fields': ('generated_by',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Nếu là tạo mới
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'is_default')
    list_filter = ('farm', 'is_default')
    search_fields = ('name', 'farm__name')
    list_editable = ('is_default',)
    fieldsets = (
        (_('Thông tin chung'), {
            'fields': ('farm', 'name', 'is_default')
        }),
        (_('Cấu hình'), {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Nếu đặt làm mặc định, bỏ mặc định của các dashboard khác cùng farm
        if obj.is_default:
            Dashboard.objects.filter(farm=obj.farm, is_default=True).exclude(pk=obj.pk).update(is_default=False)
        super().save_model(request, obj, form, change)