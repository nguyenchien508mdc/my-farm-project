# apps/approval/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ApprovalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.approval'
    verbose_name = _("Hệ thống phê duyệt")
    
    def ready(self):
        # Import signals để đăng ký với Django
        from . import signals  # noqa
        
        # Hoặc có thể đăng ký signals tại đây nếu muốn
        # from django.db.models.signals import post_save
        # from .models import ApprovalRequest
        # from .signals import handle_approval_request_status_change
        # post_save.connect(handle_approval_request_status_change, sender=ApprovalRequest)