from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', _('Chờ xử lý')),
        ('confirmed', _('Đã xác nhận')),
        ('processing', _('Đang chuẩn bị hàng')),
        ('shipped', _('Đang giao hàng')),
        ('delivered', _('Đã giao hàng')),
        ('completed', _('Hoàn thành')),
        ('cancelled', _('Đã hủy')),
    )

    PAYMENT_METHODS = (
        ('cod', _('Thanh toán khi nhận hàng')),
        ('bank_transfer', _('Chuyển khoản ngân hàng')),
        ('momo', _('Ví điện tử MoMo')),
    )

    customer = models.ForeignKey('core.User', on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(_("Trạng thái"), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(_("Phương thức thanh toán"), max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.BooleanField(_("Đã thanh toán"), default=False)
    shipping_address = models.TextField(_("Địa chỉ giao hàng"))
    contact_phone = models.CharField(_("Số điện thoại"), max_length=20)
    subtotal = models.DecimalField(_("Tổng tiền hàng"), max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(_("Giảm giá"), max_digits=12, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(_("Phí vận chuyển"), max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(_("Tổng thanh toán"), max_digits=12, decimal_places=2)
    tracking_number = models.CharField(_("Mã vận đơn"), max_length=50, blank=True)
    note = models.TextField(_("Ghi chú"), blank=True, null=True)

    class Meta:
        verbose_name = _("Đơn hàng")
        verbose_name_plural = _("Đơn hàng")
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn hàng #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('sales.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(_("Số lượng"), validators=[MinValueValidator(1)])
    price = models.DecimalField(_("Đơn giá"), max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(_("Giảm giá"), max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Mục đơn hàng")
        verbose_name_plural = _("Các mục đơn hàng")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"