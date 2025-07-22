# apps/inventory/models.py
from django.db import models
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Supplier(BaseModel):
    name = models.CharField(_("Tên nhà cung cấp"), max_length=255)
    contact_person = models.CharField(_("Người liên hệ"), max_length=100, blank=True)
    phone = models.CharField(_("Số điện thoại"), max_length=20)
    email = models.EmailField(_("Email"), blank=True)
    address = models.TextField(_("Địa chỉ"), blank=True)
    tax_code = models.CharField(_("Mã số thuế"), max_length=20, blank=True)
    rating = models.FloatField(_("Đánh giá"), null=True, blank=True)
    is_active = models.BooleanField(_("Đang hợp tác"), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Nhà cung cấp")
        verbose_name_plural = _("Nhà cung cấp")

class InventoryItemCategory(BaseModel):
    name = models.CharField(_("Danh mục"), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(_("Mô tả"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Danh mục vật tư")
        verbose_name_plural = _("Danh mục vật tư")

class InventoryItem(BaseModel):
    ITEM_TYPES = [
        ('seed', 'Hạt giống'),
        ('fertilizer', 'Phân bón'),
        ('pesticide', 'Thuốc trừ sâu'),
        ('tool', 'Công cụ'),
        ('equipment', 'Thiết bị'),
    ]

    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Lít'),
        ('ml', 'Mililit'),
        ('unit', 'Cái'),
    ]

    name = models.CharField(_("Tên vật tư"), max_length=255)
    item_type = models.CharField(_("Loại vật tư"), max_length=20, choices=ITEM_TYPES)
    category = models.ForeignKey('inventory.InventoryItemCategory', on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey('inventory.Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(_("Đơn vị"), max_length=10, choices=UNIT_CHOICES)
    current_stock = models.FloatField(_("Tồn kho hiện tại"), default=0)
    min_stock_level = models.FloatField(_("Mức tồn kho tối thiểu"), default=0)
    description = models.TextField(_("Mô tả"), blank=True)
    storage_conditions = models.TextField(_("Điều kiện bảo quản"), blank=True)
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='inventory_items', verbose_name=_("Trang trại"))


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Vật tư")
        verbose_name_plural = _("Vật tư")

class InventoryTransaction(BaseModel):
    TRANSACTION_TYPES = [
        ('purchase', 'Nhập kho'),
        ('consumption', 'Xuất kho'),
        ('adjustment', 'Điều chỉnh'),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(_("Loại giao dịch"), max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.FloatField(_("Số lượng"))
    date = models.DateField(_("Ngày giao dịch"))
    reference_number = models.CharField(_("Số tham chiếu"), max_length=50, blank=True)
    notes = models.TextField(_("Ghi chú"), blank=True)
    related_object_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('related_object_type', 'related_object_id')
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='inventory_transactions', verbose_name=_("Trang trại"))


    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.name}"

    class Meta:
        verbose_name = _("Giao dịch kho")
        verbose_name_plural = _("Giao dịch kho")