from django.db import transaction
from apps.core.models import User
from ..models.cart import Cart, CartItem
from apps.sales.models.product import Product
from apps.sales.models.voucher import Voucher

class CartService:
    @staticmethod
    def get_or_create_cart(user=None, session_key=None):
        # Lấy hoặc tạo giỏ hàng dựa vào người dùng hoặc session
        if user and user.is_authenticated:
            return Cart.objects.get_or_create(user=user)[0]
        elif session_key:
            return Cart.objects.get_or_create(session_key=session_key, user=None)[0]
        raise ValueError("Phải cung cấp user hoặc session_key")

    @staticmethod
    def add_to_cart(cart, product_id, quantity=1):
        # Thêm sản phẩm vào giỏ, nếu có rồi thì tăng số lượng
        if quantity < 1:
            raise ValueError("Số lượng tối thiểu là 1")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValueError("Sản phẩm không tồn tại")

        with transaction.atomic():
            item, created = CartItem.objects.get_or_create(
                cart=cart, product=product,
                defaults={'quantity': quantity, 'price': product.price}
            )
            if not created:
                item.quantity += quantity
                item.save()
        return item

    @staticmethod
    def update_cart_item(cart_item_id, quantity=None):
        # Cập nhật số lượng sản phẩm trong giỏ
        try:
            item = CartItem.objects.get(pk=cart_item_id)
        except CartItem.DoesNotExist:
            raise ValueError("Không tìm thấy mục giỏ hàng")

        if quantity is not None:
            if quantity < 1:
                raise ValueError("Số lượng tối thiểu là 1")
            item.quantity = quantity
            item.save()
        return item

    @staticmethod
    def remove_from_cart(cart_item_id):
        # Xóa một mục khỏi giỏ hàng
        try:
            CartItem.objects.get(pk=cart_item_id).delete()
            return True
        except CartItem.DoesNotExist:
            raise ValueError("Không tìm thấy mục giỏ hàng")

    @staticmethod
    def clear_cart(cart_id):
        # Xóa toàn bộ mục trong giỏ
        try:
            Cart.objects.get(pk=cart_id).items.all().delete()
            return True
        except Cart.DoesNotExist:
            raise ValueError("Không tìm thấy giỏ hàng")

    @staticmethod
    def get_cart_total(cart_id):
        # Tính tổng tiền của giỏ hàng
        try:
            cart = Cart.objects.get(pk=cart_id)
            total = sum(
                (item.price * item.quantity) - item.applied_discount
                for item in cart.items.all()
            )
            return total - cart.discount_amount
        except Cart.DoesNotExist:
            raise ValueError("Không tìm thấy giỏ hàng")

    @staticmethod
    def apply_voucher(cart_id, voucher_code):
        # Áp dụng mã giảm giá vào giỏ
        try:
            cart = Cart.objects.get(pk=cart_id)
            voucher = Voucher.objects.get(code=voucher_code, is_active=True)

            # Gán voucher, giảm giá tạm tính là 10 đơn vị
            cart.voucher = voucher
            cart.discount_amount = 10
            cart.save()
            return cart
        except Cart.DoesNotExist:
            raise ValueError("Không tìm thấy giỏ hàng")
        except Voucher.DoesNotExist:
            raise ValueError("Mã giảm giá không hợp lệ")

    @staticmethod
    def remove_voucher(cart_id):
        # Gỡ bỏ mã giảm giá khỏi giỏ
        try:
            cart = Cart.objects.get(pk=cart_id)
            cart.voucher = None
            cart.discount_amount = 0
            cart.save()
            return cart
        except Cart.DoesNotExist:
            raise ValueError("Không tìm thấy giỏ hàng")

    @staticmethod
    def merge_carts(user, session_cart):
        # Gộp giỏ hàng session vào giỏ người dùng sau khi đăng nhập
        if not user.is_authenticated:
            raise ValueError("Người dùng chưa đăng nhập")

        try:
            user_cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            session_cart.user = user
            session_cart.session_key = None
            session_cart.save()
            return session_cart

        with transaction.atomic():
            for item in session_cart.items.all():
                try:
                    existing_item = user_cart.items.get(product=item.product)
                    existing_item.quantity += item.quantity
                    existing_item.save()
                except CartItem.DoesNotExist:
                    item.cart = user_cart
                    item.save()
            session_cart.delete()

        return user_cart
