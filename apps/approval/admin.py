#apps\approval\admin.py
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.approval.models import ApprovalRequest


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = (
        'request_type_display', 'requester_info', 'approver_info',
        'farm_link', 'status_badge', 'request_date', 'approval_date', 'related_object_link',
    )
    list_filter = ( 'status', 'farm', 'request_date')
    search_fields = (
        'requester__username', 'requester__email', 'approver__username',
        'farm__name', 'notes', 'response_notes',
    )
    readonly_fields = ('request_date', 'approval_date', 'related_object_link')
    fieldsets = (
        (_('Thông tin cơ bản'), {'fields': ('farm', 'status', 'request_date', 'approval_date')}),
        (_('Người liên quan'), {'fields': ('requester', 'approver')}),
        (_('Đối tượng liên quan'), {'fields': ('related_object_link',)}),
        (_('Nội dung'), {'fields': ('notes', 'response_notes')}),
    )

    def request_type_display(self, obj):
        return obj.get_request_type_display()
    request_type_display.short_description = _('Loại yêu cầu')

    def requester_info(self, obj):
        return f"{obj.requester.username} ({obj.requester.email})"
    requester_info.short_description = _('Người yêu cầu')

    def approver_info(self, obj):
        return f"{obj.approver.username} ({obj.approver.email})"
    approver_info.short_description = _('Người phê duyệt')

    def farm_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:farm_farm_change', args=[obj.farm.id])
        return format_html('<a href="{}">{}</a>', url, obj.farm.name)
    farm_link.short_description = _('Nông trại')
    farm_link.admin_order_field = 'farm__name'

    def status_badge(self, obj):
        colors = {'pending': 'orange', 'approved': 'green', 'rejected': 'red', 'changes_requested': 'blue'}
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="padding:5px;background-color:{};color:#fff;border-radius:5px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = _('Trạng thái')
    status_badge.admin_order_field = 'status'

    def related_object_link(self, obj):
        if obj.related_object:
            from django.urls import reverse
            meta = obj.related_object._meta
            url = reverse(f'admin:{meta.app_label}_{meta.model_name}_change', args=[obj.related_object.id])
            return format_html('<a href="{}">{}</a>', url, obj.related_object)
        return "-"
    related_object_link.short_description = _('Đối tượng liên quan')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'requester', 'approver', 'farm', 'related_object_type',
        )

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status != 'pending':
            obj.approval_date = timezone.now()
        super().save_model(request, obj, form, change)


class ApprovalRequestInline(GenericTabularInline):
    model = ApprovalRequest
    extra = 0
    fields = ('request_type', 'status', 'requester', 'approver')
    readonly_fields = fields
    can_delete = False

