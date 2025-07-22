from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.sales.models.product import Product
from ..models.inventory import Inventory

class InventoryService:
    @staticmethod
    def create_inventory(product_id, initial_quantity=0, **kwargs):
        # Tạo bản ghi tồn kho cho sản phẩm
        try:
            product = Product.objects.get(pk=product_id)
            if hasattr(product, 'inventory'):
                raise ValidationError("Sản phẩm đã có tồn kho")
            return Inventory.objects.create(product=product, quantity=initial_quantity, **kwargs)
        except Product.DoesNotExist:
            raise ValueError("Sản phẩm không tồn tại")

    @staticmethod
    def get_inventory(product_id):
        # Lấy thông tin tồn kho của sản phẩm
        try:
            return Product.objects.get(pk=product_id).inventory
        except Product.DoesNotExist:
            raise ValueError("Sản phẩm không tồn tại")
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def update_stock(product_id, quantity_change, is_reserved=False):
        # Cập nhật số lượng tồn kho (hoặc tồn kho dự trữ)
        try:
            inventory = Inventory.objects.select_for_update().get(product_id=product_id)
            with transaction.atomic():
                if is_reserved:
                    new_reserved = inventory.reserved + quantity_change
                    if new_reserved < 0 or (quantity_change < 0 and abs(quantity_change) > inventory.reserved):
                        raise ValidationError("Không hợp lệ khi cập nhật tồn kho dự trữ")
                    inventory.reserved = new_reserved
                else:
                    if inventory.quantity + quantity_change < 0:
                        raise ValidationError("Tồn kho không đủ")
                    inventory.quantity += quantity_change
                inventory.save()
                return inventory
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def reserve_stock(product_id, quantity):
        # Dự trữ hàng (khi đặt hàng nhưng chưa xác nhận)
        if quantity <= 0:
            raise ValueError("Số lượng phải dương")
        try:
            inventory = Inventory.objects.select_for_update().get(product_id=product_id)
            with transaction.atomic():
                if inventory.quantity - inventory.reserved < quantity:
                    raise ValidationError("Không đủ hàng để dự trữ")
                inventory.reserved += quantity
                inventory.save()
                return inventory
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def release_reserved_stock(product_id, quantity):
        # Giải phóng hàng đã dự trữ (hủy đơn hàng)
        return InventoryService.update_stock(product_id, -quantity, is_reserved=True)

    @staticmethod
    def fulfill_reserved_stock(product_id, quantity):
        # Hoàn tất đơn hàng, trừ vào tồn kho và dự trữ
        try:
            inventory = Inventory.objects.select_for_update().get(product_id=product_id)
            with transaction.atomic():
                if inventory.reserved < quantity:
                    raise ValidationError("Không đủ hàng dự trữ")
                inventory.reserved -= quantity
                inventory.quantity -= quantity
                inventory.save()
                return inventory
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def restock(product_id, quantity, location=None):
        # Nhập thêm hàng vào kho
        if quantity <= 0:
            raise ValueError("Số lượng phải dương")
        try:
            inventory = Inventory.objects.get(product_id=product_id)
            with transaction.atomic():
                inventory.quantity += quantity
                inventory.last_restocked = timezone.now()
                if location:
                    inventory.location = location
                inventory.save()
                return inventory
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def check_low_stock(product_id=None):
        # Kiểm tra hàng sắp hết
        from django.db.models import F
        if product_id:
            try:
                inv = Inventory.objects.get(product_id=product_id)
                return inv.quantity <= inv.low_stock_threshold
            except Inventory.DoesNotExist:
                raise ValueError("Không tìm thấy tồn kho")
        return Inventory.objects.filter(quantity__lte=F('low_stock_threshold'))

    @staticmethod
    def get_available_quantity(product_id):
        # Lấy số lượng khả dụng (tổng - dự trữ)
        try:
            inv = Inventory.objects.get(product_id=product_id)
            return inv.quantity - inv.reserved
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def update_inventory_settings(product_id, low_stock_threshold=None, location=None):
        # Cập nhật thiết lập kho (ngưỡng cảnh báo, vị trí)
        try:
            inv = Inventory.objects.get(product_id=product_id)
            if low_stock_threshold is not None:
                if low_stock_threshold < 0:
                    raise ValueError("Ngưỡng không được âm")
                inv.low_stock_threshold = low_stock_threshold
            if location is not None:
                inv.location = location
            inv.save()
            return inv
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho")

    @staticmethod
    def transfer_stock(from_product_id, to_product_id, quantity, reason=None):
        # Chuyển hàng giữa hai sản phẩm (hoặc kho)
        if quantity <= 0:
            raise ValueError("Số lượng phải dương")
        try:
            with transaction.atomic():
                from_inv = Inventory.objects.select_for_update().get(product_id=from_product_id)
                to_inv = Inventory.objects.select_for_update().get(product_id=to_product_id)

                if from_inv.quantity < quantity:
                    raise ValidationError("Không đủ hàng để chuyển")

                from_inv.quantity -= quantity
                to_inv.quantity += quantity

                from_inv.save()
                to_inv.save()

                # Có thể ghi log chuyển kho tại đây
                return from_inv, to_inv
        except Inventory.DoesNotExist:
            raise ValueError("Không tìm thấy tồn kho của sản phẩm")
