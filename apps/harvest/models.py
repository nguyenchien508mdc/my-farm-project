# apps/harvest/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class Harvest(BaseModel):
    QUALITY_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='harvests')
    crop = models.ForeignKey('crop.Crop', on_delete=models.CASCADE, related_name='harvests')
    harvest_date = models.DateField(_("Ngày thu hoạch"))
    quantity = models.FloatField(_("Sản lượng"))
    unit = models.CharField(_("Đơn vị"), max_length=20, default='kg')
    quality = models.CharField(_("Chất lượng"), max_length=20, choices=QUALITY_CHOICES)
    notes = models.TextField(_("Ghi chú"), blank=True)
    storage_location = models.CharField(_("Nơi lưu trữ"), max_length=100, blank=True)

    def __str__(self):
        return f"Harvest of {self.crop} on {self.harvest_date}"

    class Meta:
        verbose_name = _("Thu hoạch")
        verbose_name_plural = _("Thu hoạch")