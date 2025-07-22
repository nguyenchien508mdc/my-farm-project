from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.models import BaseModel

class Voucher(BaseModel):
    DISCOUNT_TYPES = (
        ('percentage', _('Phần trăm')),
        ('fixed_amount', _('Giá trị cố định')),
    )
    
    APPLY_TO = (
        ('entire_order', _('Toàn bộ đơn hàng')),
        ('specific_products', _('Sản phẩm cụ thể')),
        ('product_categories', _('Danh mục sản phẩm')),
    )

    code = models.CharField(_("Mã voucher"), max_length=50, unique=True)
    name = models.CharField(_("Tên chương trình"), max_length=100)
    description = models.TextField(_("Mô tả"), blank=True)
    discount_type = models.CharField(_("Loại giảm giá"), max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(_("Giá trị giảm"), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    apply_to = models.CharField(_("Áp dụng cho"), max_length=20, choices=APPLY_TO)
    min_order_value = models.DecimalField(_("Giá trị đơn tối thiểu"), max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    max_discount_amount = models.DecimalField(_("Giảm tối đa"), max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(_("Ngày bắt đầu"))
    end_date = models.DateTimeField(_("Ngày kết thúc"))
    max_usage = models.PositiveIntegerField(_("Số lượt tối đa"), null=True, blank=True)
    current_usage = models.PositiveIntegerField(_("Đã sử dụng"), default=0)
    is_active = models.BooleanField(_("Kích hoạt"), default=True)
    allow_combined = models.BooleanField(_("Dùng chung voucher khác"), default=False)
    for_first_time_buyers = models.BooleanField(_("Cho khách mua lần đầu"), default=False)
    for_organic_products = models.BooleanField(_("Cho sản phẩm hữu cơ"), default=False)
    products = models.ManyToManyField('sales.Product', verbose_name=_("Sản phẩm áp dụng"), blank=True)
    categories = models.ManyToManyField('sales.ProductCategory', verbose_name=_("Danh mục áp dụng"), blank=True)

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Các voucher")
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        if self.discount_type == 'percentage' and self.discount_value > 100:
            raise ValidationError(_("Giảm giá phần trăm không thể lớn hơn 100%"))
        
        if self.start_date >= self.end_date:
            raise ValidationError(_("Ngày kết thúc phải sau ngày bắt đầu"))

class VoucherUsage(BaseModel):
    voucher = models.ForeignKey('sales.Voucher', on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('sales.Order', on_delete=models.SET_NULL, null=True)
    discount_amount = models.DecimalField(_("Số tiền giảm"), max_digits=12, decimal_places=2)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Lịch sử sử dụng voucher")
        verbose_name_plural = _("Lịch sử sử dụng voucher")
        ordering = ['-applied_at']