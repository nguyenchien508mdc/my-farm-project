# apps/approval/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver
from django.utils import timezone
from .models import ApprovalRequest
from .exceptions import InvalidRequestStatusException

# Định nghĩa các tín hiệu tùy chỉnh (custom signals)
approval_request_approved = Signal()            # tín hiệu khi yêu cầu phê duyệt được chấp nhận
approval_request_rejected = Signal()            # tín hiệu khi yêu cầu phê duyệt bị từ chối
approval_request_changes_requested = Signal()   # tín hiệu khi yêu cầu phê duyệt cần chỉnh sửa thêm
approval_request_created = Signal()             # tín hiệu khi yêu cầu phê duyệt mới được tạo

@receiver(pre_save, sender=ApprovalRequest)
def validate_approval_request_status_change(sender, instance, **kwargs):
    """
    Kiểm tra hợp lệ việc thay đổi trạng thái trước khi lưu
    """
    # Nếu là đối tượng mới (chưa tồn tại trong DB) thì không cần kiểm tra
    if instance.pk is None:
        return

    # Lấy dữ liệu gốc từ DB để so sánh trạng thái cũ
    original = ApprovalRequest.objects.get(pk=instance.pk)
    
    # Nếu trạng thái không thay đổi thì bỏ qua
    if original.status == instance.status:
        return
    
    # Định nghĩa các trạng thái hợp lệ có thể chuyển đổi tới
    valid_transitions = {
        ApprovalRequest.PENDING: [
            ApprovalRequest.APPROVED, 
            ApprovalRequest.REJECTED,
            ApprovalRequest.CHANGES_REQUESTED
        ],
        ApprovalRequest.CHANGES_REQUESTED: [
            ApprovalRequest.APPROVED,
            ApprovalRequest.REJECTED,
            ApprovalRequest.PENDING
        ]
    }
    
    # Nếu trạng thái gốc không nằm trong danh sách các trạng thái cho phép chuyển đổi
    if original.status not in valid_transitions:
        raise InvalidRequestStatusException(
            f"Không thể thay đổi trạng thái từ {original.status}"
        )
    
    # Nếu trạng thái mới không nằm trong danh sách trạng thái được phép chuyển tới
    if instance.status not in valid_transitions.get(original.status, []):
        raise InvalidRequestStatusException(
            f"Chuyển trạng thái không hợp lệ từ {original.status} sang {instance.status}"
        )

@receiver(post_save, sender=ApprovalRequest)
def handle_approval_request_status_change(sender, instance, created, **kwargs):
    """
    Phát tín hiệu phù hợp dựa trên thay đổi trạng thái của yêu cầu phê duyệt
    """
    if created:
        # Nếu là bản ghi mới tạo thì phát tín hiệu yêu cầu mới
        approval_request_created.send(
            sender=sender,
            request=instance,
            related_object=instance.related_object
        )
        return
    
    # Lấy dữ liệu gốc để so sánh trạng thái cũ
    original = ApprovalRequest.objects.get(pk=instance.pk)
    
    # Nếu trạng thái không thay đổi thì không làm gì cả
    if original.status == instance.status:
        return
    
    # Nếu trạng thái mới là đã duyệt hoặc bị từ chối thì cập nhật ngày duyệt
    if instance.status in [ApprovalRequest.APPROVED, ApprovalRequest.REJECTED]:
        instance.approval_date = timezone.now()
        instance.save(update_fields=['approval_date'])
    
    # Bảng ánh xạ trạng thái với tín hiệu tương ứng
    signal_map = {
        ApprovalRequest.APPROVED: approval_request_approved,
        ApprovalRequest.REJECTED: approval_request_rejected,
        ApprovalRequest.CHANGES_REQUESTED: approval_request_changes_requested
    }
    
    # Phát tín hiệu tương ứng với trạng thái mới
    if instance.status in signal_map:
        signal_map[instance.status].send(
            sender=sender,
            request=instance,
            related_object=instance.related_object,
            previous_status=original.status
        )
