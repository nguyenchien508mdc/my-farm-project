# apps/approval/exceptions.py
class ApprovalException(Exception):
    """Base exception for approval app"""
    pass

class InvalidApproverException(ApprovalException):
    """Raised when approver is not valid for the request"""
    pass

class InvalidRequestStatusException(ApprovalException):
    """Raised when trying to perform action on request with invalid status"""
    pass

class DuplicateRequestException(ApprovalException):
    """Raised when duplicate approval request is detected"""
    pass