# app/farm/models.py
from django.db import models
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from unidecode import unidecode
import os
from django.conf import settings

class Farm(BaseModel):
    FARM_TYPE_CHOICES = [
        ("plant", "Trồng trọt"),
        ("livestock", "Chăn nuôi"),
        ("mixed", "Kết hợp"),
    ]

    name = models.CharField(_("Tên nông trại"), max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    location = models.CharField(_("Địa điểm"), max_length=255)
    area = models.FloatField(_("Diện tích (ha)"), validators=[MinValueValidator(0)])
    farm_type = models.CharField(_("Loại hình nông trại"), max_length=20, choices=FARM_TYPE_CHOICES)
    description = models.TextField(_("Mô tả thêm"), blank=True)
    is_active = models.BooleanField(_("Đang hoạt động"), default=True)
    established_date = models.DateField(_("Ngày thành lập"), null=True, blank=True)
    logo = models.ImageField(_("Logo nông trại"), upload_to='farm_logos/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Nếu cập nhật logo mới => xóa logo cũ
        if self.pk:
            old_farm = Farm.objects.filter(pk=self.pk).first()
            if old_farm and old_farm.logo and old_farm.logo != self.logo:
                old_path = os.path.join(settings.MEDIA_ROOT, old_farm.logo.name)
                if os.path.exists(old_path):
                    os.remove(old_path)

        # Tự tạo slug nếu chưa có
        if not self.slug:
            self.slug = slugify(unidecode(self.name))

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Xóa ảnh khi xóa Farm
        if self.logo:
            logo_path = os.path.join(settings.MEDIA_ROOT, self.logo.name)
            if os.path.exists(logo_path):
                os.remove(logo_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Nông trại")
        verbose_name_plural = _("Nông trại")
        indexes = [
            models.Index(fields=['farm_type']),
            models.Index(fields=['is_active']),
        ]

class FarmMembership(BaseModel):
    ROLE_CHOICES = [
        ('manager', 'Quản lý'),
        ('assistant_manager', 'Phó quản lý'),
        ('field_supervisor', 'Giám sát đồng ruộng'),
        ('farmer', 'Nông dân'),
        ('sales', 'Nhân viên bán hàng'),
    ]
    
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    can_approve = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} @ {self.farm.name} ({self.get_role_display()})"

    class Meta:
        unique_together = ('farm', 'user')
        verbose_name = _("Thành viên nông trại")
        verbose_name_plural = _("Thành viên nông trại")
        ordering = ['-joined_date']

class FarmDocument(BaseModel):
    DOCUMENT_TYPES = [
        ('license', 'Giấy phép'),
        ('certificate', 'Chứng nhận'),
        ('contract', 'Hợp đồng'),
    ]
    
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='farm_documents/')
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.title}"

    class Meta:
        verbose_name = _("Tài liệu nông trại")
        verbose_name_plural = _("Tài liệu nông trại")