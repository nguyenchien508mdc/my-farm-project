from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Inventory(models.Model):
    product = models.OneToOneField('sales.Product', on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(_("Số lượng hiện có"), default=0)
    reserved = models.PositiveIntegerField(_("Số lượng đã đặt"), default=0)
    low_stock_threshold = models.PositiveIntegerField(_("Ngưỡng cảnh báo"), default=10)
    last_restocked = models.DateTimeField(_("Lần nhập kho cuối"), null=True, blank=True)
    location = models.CharField(_("Vị trí kho"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("Kho hàng")
        verbose_name_plural = _("Kho hàng")

    def __str__(self):
        return f"Kho của {self.product.name}"