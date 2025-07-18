from rest_framework import serializers
from ..models.cart import Cart, CartItem
from apps.core.serializers import UserSerializer
from apps.sales.serializers.product_serializer import ProductSerializer
from apps.sales.serializers.voucher_serializer import VoucherSerializer

# ----- Chi tiết mặt hàng trong giỏ hàng -----
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Thông tin sản phẩm
    total_price = serializers.SerializerMethodField()  # Tổng tiền sau giảm giá

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price', 'applied_discount', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'price', 'created_at', 'updated_at', 'total_price']

    def get_total_price(self, obj):
        # Tính tổng tiền = giá * số lượng - giảm giá áp dụng
        return (obj.price * obj.quantity) - obj.applied_discount

# ----- Tạo/cập nhật mặt hàng trong giỏ -----
class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Số lượng phải lớn hơn hoặc bằng 1")
        return value

# ----- Hiển thị giỏ hàng -----
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Thông tin người dùng
    items = CartItemSerializer(many=True, read_only=True)  # Danh sách mặt hàng
    voucher = VoucherSerializer(read_only=True)  # Voucher áp dụng (nếu có)
    subtotal = serializers.SerializerMethodField()  # Tổng tiền chưa trừ voucher
    total = serializers.SerializerMethodField()  # Tổng tiền sau trừ voucher

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'voucher', 'discount_amount', 'note', 'items', 'subtotal', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'discount_amount', 'created_at', 'updated_at', 'subtotal', 'total']

    def get_subtotal(self, obj):
        # Tổng tiền = tổng giá các mặt hàng (giá * số lượng)
        return sum(item.price * item.quantity for item in obj.items.all())

    def get_total(self, obj):
        # Tổng tiền sau giảm = subtotal - discount_amount
        return self.get_subtotal(obj) - obj.discount_amount

# ----- Áp voucher cho giỏ hàng -----
class CartVoucherSerializer(serializers.Serializer):
    voucher_code = serializers.CharField(max_length=50, required=False)

    def validate_voucher_code(self, value):
        # Cho phép voucher_code rỗng (None)
        if value == "":
            return None
        return value

# ----- Cập nhật số lượng nhiều mặt hàng cùng lúc -----
class CartItemBulkUpdateSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(child_fields={
            'product_id': serializers.IntegerField(),
            'quantity': serializers.IntegerField(min_value=1)
        })
    )

    def validate(self, data):
        if not data.get('items'):
            raise serializers.ValidationError("Danh sách sản phẩm không được trống")
        return data
