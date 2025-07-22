# apps/approval/services.py
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ApprovalRequest
from .exceptions import (
    InvalidApproverException,
    InvalidRequestStatusException,
    DuplicateRequestException
)
from .utils import check_pending_requests_exists

class ApprovalService:
    @staticmethod
    def create_request(farm, requester, approver, related_object, notes=""):
        """
        Tạo yêu cầu phê duyệt mới
        """
        """Tạo yêu cầu phê duyệt mới với kiểm tra"""
        if check_pending_requests_exists(related_object):
            raise DuplicateRequestException("Đã có yêu cầu chờ phê duyệt cho đối tượng này")
        
        content_type = ContentType.objects.get_for_model(related_object)
        
        return ApprovalRequest.objects.create(
            farm=farm,
            requester=requester,
            approver=approver,
            related_object_type=content_type,
            related_object_id=related_object.id,
            notes=notes,
            status=ApprovalRequest.PENDING
        )

    @staticmethod
    def approve_request(request_id, approver, response_notes=""):
        """
        Phê duyệt yêu cầu
        """
        """Tạo yêu cầu phê duyệt mới với kiểm tra"""
        request = ApprovalRequest.objects.get(id=request_id)
        if request.approver != approver:
            raise InvalidApproverException("Người phê duyệt không hợp lệ")
        
        request.status = ApprovalRequest.APPROVED
        request.approval_date = timezone.now()
        request.response_notes = response_notes
        request.save()
        
        return request

    @staticmethod
    def reject_request(request_id, approver, response_notes=""):
        """
        Từ chối yêu cầu
        """
        request = ApprovalRequest.objects.get(id=request_id)
        if request.approver != approver:
            raise InvalidApproverException("Người phê duyệt không hợp lệ")
        
        request.status = ApprovalRequest.REJECTED
        request.approval_date = timezone.now()
        request.response_notes = response_notes
        request.save()
        
        return request