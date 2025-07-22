from django.db import transaction
from django.core.exceptions import ValidationError
from apps.core.models import User
from apps.sales.models.product import Product
from ..models.order import Order, OrderItem

class OrderService:
    @staticmethod
    def create_order(customer, payment_method, shipping_address, contact_phone, cart_items,
                     discount_amount=0, shipping_fee=0, **kwargs):
        # Tạo đơn hàng mới từ các mục trong giỏ hàng
        if not isinstance(customer, User):
            raise ValueError("Khách hàng không hợp lệ")
        if payment_method not in dict(Order.PAYMENT_METHODS):
            raise ValueError("Phương thức thanh toán không hợp lệ")

        with transaction.atomic():
            subtotal = sum(i.price * i.quantity for i in cart_items)
            total = subtotal - discount_amount + shipping_fee

            order = Order.objects.create(
                customer=customer,
                payment_method=payment_method,
                shipping_address=shipping_address,
                contact_phone=contact_phone,
                subtotal=subtotal,
                discount_amount=discount_amount,
                shipping_fee=shipping_fee,
                total=total,
                **kwargs
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price,
                    discount_amount=item.applied_discount
                )
            return order

    @staticmethod
    def update_order_status(order_id, new_status, **kwargs):
        # Cập nhật trạng thái đơn hàng
        if new_status not in dict(Order.STATUS_CHOICES):
            raise ValueError("Trạng thái không hợp lệ")

        try:
            order = Order.objects.get(pk=order_id)

            if order.status == 'cancelled' and new_status != 'cancelled':
                raise ValidationError("Không thể thay đổi trạng thái đơn hàng đã hủy")

            if new_status == 'completed' and order.status != 'delivered':
                raise ValidationError("Đơn hàng phải được giao trước khi hoàn tất")

            order.status = new_status
            if 'tracking_number' in kwargs:
                order.tracking_number = kwargs['tracking_number']
            if new_status == 'completed':
                order.payment_status = True

            order.save()
            return order
        except Order.DoesNotExist:
            raise ValueError("Không tìm thấy đơn hàng")

    @staticmethod
    def cancel_order(order_id, reason=None):
        # Hủy đơn hàng
        try:
            order = Order.objects.get(pk=order_id)

            if order.status == 'cancelled':
                return order
            if order.status in ['delivered', 'completed']:
                raise ValidationError("Không thể hủy đơn hàng đã giao hoặc hoàn tất")

            order.status = 'cancelled'
            order.save()
            # Có thể thêm: hoàn tiền, thông báo, ghi log...
            return order
        except Order.DoesNotExist:
            raise ValueError("Không tìm thấy đơn hàng")

    @staticmethod
    def get_order_details(order_id):
        # Lấy thông tin chi tiết đơn hàng kèm sản phẩm
        try:
            return Order.objects.select_related('customer').prefetch_related('items__product').get(pk=order_id)
        except Order.DoesNotExist:
            raise ValueError("Không tìm thấy đơn hàng")

    @staticmethod
    def get_customer_orders(customer_id, limit=None):
        # Lấy danh sách đơn hàng của khách
        qs = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
        return qs[:limit] if limit else qs

    @staticmethod
    def add_order_item(order_id, product_id, quantity, price, discount_amount=0):
        # Thêm sản phẩm vào đơn hàng
        if quantity < 1:
            raise ValueError("Số lượng tối thiểu là 1")
        try:
            order = Order.objects.get(pk=order_id)
            product = Product.objects.get(pk=product_id)

            if order.status != 'pending':
                raise ValidationError("Chỉ thêm sản phẩm khi đơn đang chờ xử lý")

            with transaction.atomic():
                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price,
                    discount_amount=discount_amount
                )
                OrderService._recalculate_order_totals(order)
                return item
        except Order.DoesNotExist:
            raise ValueError("Không tìm thấy đơn hàng")
        except Product.DoesNotExist:
            raise ValueError("Sản phẩm không tồn tại")

    @staticmethod
    def update_order_item(order_item_id, quantity=None, price=None, discount_amount=None):
        # Cập nhật sản phẩm trong đơn hàng
        try:
            item = OrderItem.objects.select_related('order').get(pk=order_item_id)
            if item.order.status != 'pending':
                raise ValidationError("Chỉ sửa sản phẩm khi đơn đang chờ xử lý")

            with transaction.atomic():
                if quantity is not None:
                    if quantity < 1:
                        raise ValueError("Số lượng tối thiểu là 1")
                    item.quantity = quantity
                if price is not None:
                    item.price = price
                if discount_amount is not None:
                    item.discount_amount = discount_amount
                item.save()
                OrderService._recalculate_order_totals(item.order)
                return item
        except OrderItem.DoesNotExist:
            raise ValueError("Không tìm thấy sản phẩm trong đơn")

    @staticmethod
    def _recalculate_order_totals(order):
        # Tính lại tổng đơn hàng
        items = order.items.all()
        order.subtotal = sum(i.price * i.quantity for i in items)
        order.total = order.subtotal - order.discount_amount + order.shipping_fee
        order.save()

    @staticmethod
    def update_payment_status(order_id, is_paid):
        # Cập nhật trạng thái thanh toán
        try:
            order = Order.objects.get(pk=order_id)
            order.payment_status = is_paid
            order.save()
            return order
        except Order.DoesNotExist:
            raise ValueError("Không tìm thấy đơn hàng")

    @staticmethod
    def get_orders_by_status(status, limit=None):
        # Lấy danh sách đơn theo trạng thái
        if status not in dict(Order.STATUS_CHOICES):
            raise ValueError("Trạng thái không hợp lệ")
        qs = Order.objects.filter(status=status).order_by('-created_at')
        return qs[:limit] if limit else qs
