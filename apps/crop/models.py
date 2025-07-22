# apps/crop/models.py
from django.db import models
from apps.core.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class CropType(BaseModel):
    name = models.CharField(_("Tên loại cây"), max_length=100)
    scientific_name = models.CharField(_("Tên khoa học"), max_length=100, blank=True)
    description = models.TextField(_("Mô tả"), blank=True)
    growth_duration = models.PositiveIntegerField(_("Thời gian sinh trưởng (ngày)"))
    optimal_temperature_min = models.FloatField(_("Nhiệt độ tối thiểu (°C)"))
    optimal_temperature_max = models.FloatField(_("Nhiệt độ tối đa (°C)"))
    optimal_ph_min = models.FloatField(_("Độ pH tối thiểu"), validators=[MinValueValidator(0), MaxValueValidator(14)])
    optimal_ph_max = models.FloatField(_("Độ pH tối đa"), validators=[MinValueValidator(0), MaxValueValidator(14)])
    image = models.ImageField(_("Hình ảnh"), upload_to='crop_types/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Loại cây trồng")
        verbose_name_plural = _("Loại cây trồng")

class Crop(BaseModel):
    STATUS_CHOICES = [
        ('planned', 'Dự kiến trồng'),
        ('seedling', 'Cây giống'),
        ('growing', 'Đang phát triển'),
        ('harvested', 'Đã thu hoạch'),
        ('failed', 'Thất bại'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='crops')
    crop_type = models.ForeignKey('crop.CropType', on_delete=models.PROTECT, related_name='crops')
    variety = models.CharField(_("Giống cây"), max_length=100, blank=True)
    status = models.CharField(_("Trạng thái"), max_length=20, choices=STATUS_CHOICES, default='planned')
    planting_date = models.DateField(_("Ngày trồng"), null=True, blank=True)
    harvest_date = models.DateField(_("Ngày thu hoạch"), null=True, blank=True)
    area = models.FloatField(_("Diện tích (ha)"), validators=[MinValueValidator(0)])
    expected_yield = models.FloatField(_("Năng suất dự kiến (tấn/ha)"), null=True, blank=True)
    actual_yield = models.FloatField(_("Năng suất thực tế (tấn/ha)"), null=True, blank=True)
    notes = models.TextField(_("Ghi chú"), blank=True)

    def __str__(self):
        return f"{self.crop_type.name} - {self.get_status_display()}"

    class Meta:
        verbose_name = _("Cây trồng")
        verbose_name_plural = _("Cây trồng")
        ordering = ['-planting_date']

class CropStage(BaseModel):
    crop = models.ForeignKey('crop.Crop', on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(_("Giai đoạn"), max_length=100)
    start_date = models.DateField(_("Ngày bắt đầu"))
    end_date = models.DateField(_("Ngày kết thúc"), null=True, blank=True)
    description = models.TextField(_("Mô tả"), blank=True)
    completed = models.BooleanField(_("Hoàn thành"), default=False)

    def __str__(self):
        return f"{self.crop} - {self.name}"

    class Meta:
        verbose_name = _("Giai đoạn cây trồng")
        verbose_name_plural = _("Giai đoạn cây trồng")