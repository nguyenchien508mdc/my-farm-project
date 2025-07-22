from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class Cart(BaseModel):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='cart', verbose_name=_("Người dùng"), null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    voucher = models.ForeignKey('sales.Voucher', on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(_("Tổng giảm giá"), max_digits=12, decimal_places=2, default=0)
    note = models.TextField(_("Ghi chú"), blank=True)

    class Meta:
        verbose_name = _("Giỏ hàng")
        verbose_name_plural = _("Giỏ hàng")

    def __str__(self):
        return f"Giỏ hàng #{self.id}"

class CartItem(BaseModel):
    cart = models.ForeignKey('sales.Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('sales.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Số lượng"), default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(_("Đơn giá"), max_digits=12, decimal_places=2, editable=False)
    applied_discount = models.DecimalField(_("Giảm giá"), max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Mục giỏ hàng")
        verbose_name_plural = _("Các mục giỏ hàng")
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"