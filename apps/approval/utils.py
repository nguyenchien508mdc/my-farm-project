# apps/approval/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import ApprovalRequest

def get_content_type_for_model(model):
    """Lấy ContentType cho model mà không cần import model vào app approval"""
    return ContentType.objects.get_for_model(model)

def check_pending_requests_exists(obj):
    """Kiểm tra nếu đã có yêu cầu chờ phê duyệt cho object này"""
    content_type = ContentType.objects.get_for_model(obj)
    return ApprovalRequest.objects.filter(
        related_object_type=content_type,
        related_object_id=obj.id,
        status=ApprovalRequest.PENDING
    ).exists()

def get_approval_history(obj, limit=10):
    """Lấy lịch sử phê duyệt cho một object"""
    content_type = ContentType.objects.get_for_model(obj)
    return ApprovalRequest.objects.filter(
        related_object_type=content_type,
        related_object_id=obj.id
    ).order_by('-request_date')[:limit]