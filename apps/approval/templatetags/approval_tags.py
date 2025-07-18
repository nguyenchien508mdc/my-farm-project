from django import template
from django.contrib.contenttypes.models import ContentType
from apps.approval.models import ApprovalRequest

register = template.Library()

@register.simple_tag
def get_pending_approvals(user):
    return ApprovalRequest.objects.filter(
        approver=user,
        status='pending'
    ).count()

@register.simple_tag
def has_pending_approval(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return ApprovalRequest.objects.filter(
        related_object_type=content_type,
        related_object_id=obj.id,
        status='pending'
    ).exists()

@register.filter
def status_badge_color(status):
    color_map = {
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'changes_requested': 'info',
    }
    return color_map.get(status, 'secondary')