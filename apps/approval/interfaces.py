from django.contrib.contenttypes.models import ContentType
from .services import ApprovalService
from .models import ApprovalRequest
from .exceptions import (
    ApprovalException,
    InvalidApproverException,
    InvalidRequestStatusException,
    DuplicateRequestException
)
from .signals import (
    approval_request_created,
    approval_request_approved,
    approval_request_rejected,
    approval_request_changes_requested
)

class ApprovalSystem:
    """
    Giao diện công khai (public interface) cho hệ thống phê duyệt,
    các app khác nên sử dụng interface này để thao tác phê duyệt.
    Tất cả các thao tác liên quan đến phê duyệt đều phải qua đây.
    """
    
    @staticmethod
    def create_request(farm, requester, approver, obj, notes="", check_duplicates=True):
        """
        Tạo mới một yêu cầu phê duyệt

        Args:
            farm: Đối tượng nông trại (Farm)
            requester: Người tạo yêu cầu (User)
            approver: Người phê duyệt (User)
            obj: Đối tượng cần phê duyệt (bất kỳ instance model nào)
            notes: Ghi chú thêm cho yêu cầu (tuỳ chọn)
            check_duplicates: Kiểm tra trùng yêu cầu đang chờ (mặc định True)
        
        Returns:
            Trả về instance của ApprovalRequest vừa tạo
        
        Raises:
            DuplicateRequestException: Nếu phát hiện yêu cầu trùng lặp đang chờ
            ApprovalException: Ngoại lệ chung cho các lỗi liên quan đến phê duyệt
        """
        try:
            # Gọi service xử lý tạo request
            request = ApprovalService.create_request(
                farm=farm,
                requester=requester,
                approver=approver,
                related_object=obj,
                notes=notes,
                check_duplicates=check_duplicates
            )
            
            # Gửi tín hiệu khi tạo yêu cầu thành công
            approval_request_created.send(
                sender=ApprovalRequest,
                request=request,
                related_object=obj
            )
            
            return request
            
        except Exception as e:
            # Bắt lỗi và chuyển thành ApprovalException
            raise ApprovalException(f"Tạo yêu cầu phê duyệt thất bại: {str(e)}")

    @staticmethod
    def approve_request(request_id, approver, response_notes=""):
        """
        Phê duyệt một yêu cầu đã tồn tại

        Args:
            request_id: ID của yêu cầu cần phê duyệt
            approver: Người phê duyệt (User)
            response_notes: Ghi chú phản hồi khi phê duyệt (tuỳ chọn)
        
        Returns:
            Trả về instance ApprovalRequest đã cập nhật
        
        Raises:
            InvalidApproverException: Nếu người phê duyệt không đúng
            InvalidRequestStatusException: Nếu trạng thái yêu cầu không phải đang chờ
            ApprovalException: Lỗi chung liên quan phê duyệt
        """
        try:
            request = ApprovalService.approve_request(
                request_id=request_id,
                approver=approver,
                response_notes=response_notes
            )
            return request
            
        except Exception as e:
            raise ApprovalException(f"Phê duyệt yêu cầu thất bại: {str(e)}")

    @staticmethod
    def reject_request(request_id, approver, response_notes=""):
        """
        Từ chối một yêu cầu đã tồn tại

        Args:
            request_id: ID của yêu cầu cần từ chối
            approver: Người từ chối (User)
            response_notes: Ghi chú phản hồi khi từ chối (tuỳ chọn)
        
        Returns:
            Trả về instance ApprovalRequest đã cập nhật
        
        Raises:
            InvalidApproverException: Nếu người từ chối không đúng
            InvalidRequestStatusException: Nếu trạng thái yêu cầu không phải đang chờ
            ApprovalException: Lỗi chung liên quan phê duyệt
        """
        try:
            request = ApprovalService.reject_request(
                request_id=request_id,
                approver=approver,
                response_notes=response_notes
            )
            return request
            
        except Exception as e:
            raise ApprovalException(f"Từ chối yêu cầu thất bại: {str(e)}")

    @staticmethod
    def get_requests_for_object(obj, status=None):
        """
        Lấy danh sách các yêu cầu phê duyệt liên quan đến một đối tượng cụ thể

        Args:
            obj: Đối tượng liên quan
            status: Lọc theo trạng thái (tuỳ chọn)
        
        Returns:
            QuerySet chứa các ApprovalRequest phù hợp
        """
        content_type = ContentType.objects.get_for_model(obj)
        queryset = ApprovalRequest.objects.filter(
            related_object_type=content_type,
            related_object_id=obj.id
        )
        
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-request_date')

    @staticmethod
    def get_pending_requests_for_approver(approver):
        """
        Lấy danh sách các yêu cầu đang chờ phê duyệt dành cho một người phê duyệt cụ thể

        Args:
            approver: Người phê duyệt (User)
        
        Returns:
            QuerySet chứa các yêu cầu đang chờ (pending) của approver
        """
        return ApprovalRequest.objects.filter(
            approver=approver,
            status=ApprovalRequest.PENDING
        ).order_by('-request_date')

    @staticmethod
    def connect_approval_handler(receiver_func, sender_model=None):
        """
        Kết nối hàm xử lý khi yêu cầu được phê duyệt (signal handler)

        Args:
            receiver_func: Hàm nhận tín hiệu
            sender_model: Model cụ thể để lọc (tuỳ chọn)
        """
        approval_request_approved.connect(
            receiver_func,
            sender=sender_model,
            weak=False
        )

    @staticmethod
    def connect_rejection_handler(receiver_func, sender_model=None):
        """
        Kết nối hàm xử lý khi yêu cầu bị từ chối (signal handler)

        Args:
            receiver_func: Hàm nhận tín hiệu
            sender_model: Model cụ thể để lọc (tuỳ chọn)
        """
        approval_request_rejected.connect(
            receiver_func,
            sender=sender_model,
            weak=False
        )

# Tạo instance duy nhất (singleton) để tiện dùng chung
approval_system = ApprovalSystem()
