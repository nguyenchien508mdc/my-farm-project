from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from ..models.voucher import Voucher, VoucherUsage
from ..models.order import Order
from ..models.cart import Cart
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..models.voucher import Voucher, VoucherUsage
from apps.sales.models.order import Order, OrderItem
from apps.core.models import User

class VoucherService:
    @staticmethod
    def create_voucher(**kwargs) -> Voucher:
        voucher = Voucher(**kwargs)
        voucher.full_clean()
        voucher.save()
        return voucher

    @staticmethod
    def update_voucher(voucher_id: int, **kwargs) -> Voucher:
        try:
            voucher = Voucher.objects.get(id=voucher_id)
            for key, value in kwargs.items():
                setattr(voucher, key, value)
            voucher.full_clean()
            voucher.save()
            return voucher
        except Voucher.DoesNotExist:
            raise ObjectDoesNotExist(_("Không tìm thấy voucher"))

    @staticmethod
    def validate_voucher(code: str, user=None, order=None, order_items=None, current_time=None) -> dict:
        current_time = current_time or timezone.now()

        try:
            voucher = Voucher.objects.get(code=code)
        except Voucher.DoesNotExist:
            return {'is_valid': False, 'message': _("Mã voucher không tồn tại")}

        if not voucher.is_active:
            return {'is_valid': False, 'message': _("Voucher đã bị vô hiệu hóa")}
        if current_time < voucher.start_date:
            return {'is_valid': False, 'message': _("Voucher chưa có hiệu lực")}
        if current_time > voucher.end_date:
            return {'is_valid': False, 'message': _("Voucher đã hết hạn")}
        if voucher.max_usage and voucher.current_usage >= voucher.max_usage:
            return {'is_valid': False, 'message': _("Voucher đã hết lượt sử dụng")}

        if user:
            if voucher.for_first_time_buyers and user.orders.filter(status='completed').exists():
                return {'is_valid': False, 'message': _("Voucher chỉ dành cho khách hàng mới")}
            if VoucherUsage.objects.filter(voucher=voucher, user=user).exists():
                return {'is_valid': False, 'message': _("Bạn đã sử dụng voucher này rồi")}

        if order:
            if voucher.min_order_value and order.subtotal < voucher.min_order_value:
                return {'is_valid': False, 'message': _("Đơn hàng chưa đạt giá trị tối thiểu")}
            if not voucher.allow_combined and order.vouchers.exists():
                return {'is_valid': False, 'message': _("Không thể áp dụng đồng thời nhiều voucher")}

        if order_items and voucher.apply_to != 'entire_order':
            applicable_items = VoucherService._get_applicable_items(voucher, order_items)
            if not applicable_items:
                return {'is_valid': False, 'message': _("Voucher không áp dụng cho sản phẩm trong đơn hàng")}

        discount = VoucherService._calculate_discount(voucher, order, order_items)
        return {'is_valid': True, 'voucher': voucher, 'discount_amount': discount, 'message': _("Áp dụng hợp lệ")}

    @staticmethod
    def _get_applicable_items(voucher: Voucher, items: list[OrderItem]) -> list[OrderItem]:
        # Giả định sẽ có logic liên kết voucher với sản phẩm/danh mục ở đây
        applicable = []
        for item in items:
            if voucher.for_organic_products and not item.product.is_organic:
                continue
            applicable.append(item)
        return applicable

    @staticmethod
    def _calculate_discount(voucher: Voucher, order=None, order_items=None) -> float:
        if not order and not order_items:
            return 0

        if voucher.apply_to == 'entire_order' and order:
            base = order.subtotal
        else:
            applicable = VoucherService._get_applicable_items(voucher, order_items)
            base = sum(item.price * item.quantity for item in applicable)

        if voucher.discount_type == 'percentage':
            discount = base * voucher.discount_value / 100
            if voucher.max_discount_amount:
                discount = min(discount, voucher.max_discount_amount)
        else:
            discount = min(voucher.discount_value, base)

        return discount

    @staticmethod
    @transaction.atomic
    def apply_voucher_to_order(code: str, order: Order, user=None) -> dict:
        result = VoucherService.validate_voucher(code, user=user, order=order, order_items=order.items.all())
        if not result['is_valid']:
            return {'success': False, 'message': result['message']}

        voucher, discount = result['voucher'], result['discount_amount']
        order.discount_amount = discount
        order.total = order.subtotal - discount + order.shipping_fee
        order.save()

        VoucherUsage.objects.create(voucher=voucher, user=user, order=order, discount_amount=discount)
        voucher.current_usage += 1
        voucher.save()

        return {'success': True, 'voucher': voucher, 'discount_amount': discount, 'message': _("Áp dụng thành công")}

    @staticmethod
    def get_user_vouchers(user: User, include_used=False):
        vouchers = Voucher.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        if not include_used:
            used = VoucherUsage.objects.filter(user=user).values_list('voucher_id', flat=True)
            vouchers = vouchers.exclude(id__in=used)

        return vouchers.order_by('-start_date')

    @staticmethod
    def get_voucher_usage_history(voucher_id: int):
        return VoucherUsage.objects.filter(
            voucher_id=voucher_id
        ).select_related('user', 'order').order_by('-applied_at')


class VoucherUsageService:
    @staticmethod
    def create_voucher_usage(voucher: Voucher, discount_amount: float, user=None, order=None) -> VoucherUsage:
        usage = VoucherUsage(voucher=voucher, user=user, order=order, discount_amount=discount_amount)
        usage.full_clean()
        usage.save()
        voucher.current_usage += 1
        voucher.save()
        return usage

    @staticmethod
    def get_user_voucher_history(user_id: int):
        return VoucherUsage.objects.filter(user_id=user_id)\
            .select_related('voucher', 'order').order_by('-applied_at')

    @staticmethod
    def get_order_voucher_usages(order_id: int):
        return VoucherUsage.objects.filter(order_id=order_id)\
            .select_related('voucher').order_by('applied_at')
