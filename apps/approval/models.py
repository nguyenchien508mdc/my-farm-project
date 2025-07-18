# apps/approval/models.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class ApprovalRequest(BaseModel):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CHANGES_REQUESTED = 'changes_requested'
    
    STATUS_CHOICES = [
        (PENDING, 'Chờ duyệt'),
        (APPROVED, 'Đã duyệt'),
        (REJECTED, 'Từ chối'),
        (CHANGES_REQUESTED, 'Yêu cầu thay đổi'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='approval_requests')
    requester = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='requests_made')
    approver = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='requests_to_approve')
    status = models.CharField(_("Trạng thái"), max_length=20, choices=STATUS_CHOICES, default=PENDING)
    request_date = models.DateTimeField(_("Ngày yêu cầu"), auto_now_add=True)
    approval_date = models.DateTimeField(_("Ngày phê duyệt"), null=True, blank=True)
    related_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    related_object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('related_object_type', 'related_object_id')
    notes = models.TextField(_("Ghi chú yêu cầu"), blank=True)
    response_notes = models.TextField(_("Ghi chú phản hồi"), blank=True)

    def __str__(self):
        return f"Yêu cầu phê duyệt #{self.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = _("Yêu cầu phê duyệt")
        verbose_name_plural = _("Yêu cầu phê duyệt")
        ordering = ['-request_date']
        indexes = [
            models.Index(fields=['farm', 'status']),
            models.Index(fields=['requester', 'approver']),
        ]