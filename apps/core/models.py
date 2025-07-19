# apps/core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices

class Role(TextChoices):
    ADMIN = 'admin', _('Quản trị viên')
    STAFF = 'staff', _('Nhân viên')
    CUSTOMER = 'customer', _('Khách hàng')

class User(AbstractUser):
    phone_number = models.CharField(_("Số điện thoại"), max_length=20, blank=True, null=True)
    address = models.TextField(_("Địa chỉ"), blank=True, null=True)
    is_verified = models.BooleanField(_("Đã xác minh"), default=False)
    date_of_birth = models.DateField(_("Ngày sinh"), blank=True, null=True)
    profile_picture = models.ImageField(_("Ảnh đại diện"), upload_to="user_profiles/", blank=True, null=True)
    role = models.CharField(_("Vai trò"), max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    farms = models.ManyToManyField('farm.Farm', through='farm.FarmMembership', blank=True, through_fields=('user', 'farm'))
    current_farm = models.ForeignKey('farm.Farm', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_users')

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = _("Người dùng")
        verbose_name_plural = _("Người dùng")

class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Ngày tạo"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Cập nhật lần cuối"), auto_now=True)
    created_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='+')

    class Meta:
        abstract = True

class Configuration(BaseModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.key
    
    class Meta:
        verbose_name = _("Cấu hình hệ thống")
        verbose_name_plural = _("Các cấu hình hệ thống")


    @classmethod
    def get_value(cls, key, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default
