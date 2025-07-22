# apps/analytics/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class Report(BaseModel):
    REPORT_TYPES = [
        ('production', 'Sản xuất'),
        ('financial', 'Tài chính'),
        ('inventory', 'Tồn kho'),
        ('sales', 'Bán hàng'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(_("Loại báo cáo"), max_length=20, choices=REPORT_TYPES)
    title = models.CharField(_("Tiêu đề"), max_length=255)
    start_date = models.DateField(_("Từ ngày"))
    end_date = models.DateField(_("Đến ngày"))
    generated_at = models.DateTimeField(_("Ngày tạo"), auto_now_add=True)
    generated_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    file = models.FileField(_("File báo cáo"), upload_to='reports/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Báo cáo")
        verbose_name_plural = _("Báo cáo")

class Dashboard(BaseModel):
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='dashboards')
    name = models.CharField(_("Tên dashboard"), max_length=100)
    config = models.JSONField(_("Cấu hình"))
    is_default = models.BooleanField(_("Mặc định"), default=False)

    def __str__(self):
        return f"{self.farm.name} - {self.name}"

    class Meta:
        verbose_name = _("Bảng điều khiển")
        verbose_name_plural = _("Bảng điều khiển")