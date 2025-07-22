# | Serializer                        | Mục đích sử dụng                  |
# | --------------------------------- | --------------------------------- |
# | `OrderSerializer`                 | Hiển thị chi tiết đơn hàng        |
# | `OrderCreateSerializer`           | Tạo đơn hàng mới từ khách hàng    |
# | `OrderUpdateStatusSerializer`     | Cập nhật trạng thái đơn hàng      |
# | `OrderItemSerializer`             | Hiển thị mặt hàng trong đơn hàng  |
# | `OrderItemCreateUpdateSerializer` | Tạo/cập nhật mặt hàng đơn hàng    |
# | `OrderPaymentSerializer`          | Cập nhật thông tin thanh toán     |
# | `OrderStatusSerializer`           | Trạng thái đơn hàng (dropdown)    |
# | `PaymentMethodSerializer`         | Phương thức thanh toán (dropdown) |


from rest_framework import serializers
from django.utils import timezone
from ..models.order import Order, OrderItem
from apps.core.serializers import UserSerializer
from apps.sales.serializers.product_serializer import ProductSerializer


# Trạng thái đơn hàng
class OrderStatusSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': str(instance[1])}

# Phương thức thanh toán
class PaymentMethodSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': str(instance[1])}

# Hiển thị mặt hàng trong đơn hàng
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'discount_amount', 'total_price']
        read_only_fields = ['id', 'price', 'total_price']

    def get_total_price(self, obj):
        return (obj.price * obj.quantity) - obj.discount_amount

# Tạo/cập nhật mặt hàng
class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Số lượng phải lớn hơn 0")
        return value

# Hiển thị đơn hàng chi tiết
class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    can_cancel = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'status', 'status_display', 'payment_method', 'payment_method_display',
            'payment_status', 'shipping_address', 'contact_phone',
            'subtotal', 'discount_amount', 'shipping_fee', 'total',
            'tracking_number', 'items', 'can_cancel', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'subtotal', 'total', 'created_at', 'updated_at']

    def get_can_cancel(self, obj):
        return obj.status in ['pending', 'confirmed']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateUpdateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'payment_method', 'shipping_address', 'contact_phone', 'items']

    def validate(self, data):
        if not data.get('items'):
            raise serializers.ValidationError({"items": "Đơn hàng phải có ít nhất một sản phẩm"})
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        # Tạo các mặt hàng
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Tính tổng đơn hàng
        order.subtotal = sum(item.price * item.quantity for item in order.items.all())
        order.total = order.subtotal - order.discount_amount + order.shipping_fee
        order.save()

        return order

class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['processing', 'cancelled'],
            'processing': ['shipped'],
            'shipped': ['delivered'],
            'delivered': ['completed'],
        }
        current = self.instance.status
        if value not in transitions.get(current, []):
            raise serializers.ValidationError(f"Không thể chuyển từ {current} sang {value}")
        return value

class OrderPaymentSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHODS)
    payment_status = serializers.BooleanField(required=False)
    payment_details = serializers.JSONField(required=False)

    def validate(self, data):
        if data.get('payment_status') and not data.get('payment_method'):
            raise serializers.ValidationError("Phải chọn phương thức thanh toán khi cập nhật trạng thái")
        return data
