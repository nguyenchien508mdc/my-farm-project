from rest_framework import serializers
from apps.sales.models.cart import Cart, CartItem
from apps.sales.serializers.product_serializer import ProductSerializer
from apps.sales.serializers.voucher_serializer import VoucherSerializer
from apps.core.serializers import UserSerializer

# ✅ Serializer cho từng món hàng trong giỏ
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Thông tin sản phẩm (dạng nested)
    total_price = serializers.SerializerMethodField()  # Tổng tiền sau giảm giá

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'quantity', 'price',
            'applied_discount', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return max((obj.price * obj.quantity) - obj.applied_discount, 0)

# ✅ Serializer cho giỏ hàng
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)      # Danh sách item trong giỏ
    user = UserSerializer(read_only=True)                      # Người dùng (nếu có)
    voucher = VoucherSerializer(read_only=True)                # Mã giảm giá
    total = serializers.SerializerMethodField()                # Tổng tiền toàn bộ giỏ

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'session_key', 'voucher',
            'discount_amount', 'note', 'items',
            'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total(self, obj):
        # Tính tổng tiền tất cả item trừ đi tổng giảm giá
        items_total = sum(
            (item.price * item.quantity) - item.applied_discount
            for item in obj.items.all()
        )
        return max(items_total - obj.discount_amount, 0)

# ✅ Dùng khi thêm/sửa item trong giỏ
class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Số lượng tối thiểu là 1")
        return value

# ✅ Dùng để áp dụng mã giảm giá cho giỏ hàng
class CartVoucherSerializer(serializers.Serializer):
    voucher_code = serializers.CharField(max_length=50)
