# | Serializer                      | Mục đích sử dụng                     |
# | ------------------------------- | ------------------------------------ |
# | `VoucherSerializer`             | Hiển thị chi tiết phiếu giảm giá     |
# | `VoucherCreateUpdateSerializer` | Tạo / cập nhật thông tin phiếu       |
# | `VoucherUsageSerializer`        | Lịch sử sử dụng mã giảm giá          |
# | `VoucherApplySerializer`        | Gửi mã để kiểm tra và áp dụng        |
# | `VoucherValidationSerializer`   | Phản hồi kết quả áp dụng mã giảm giá |
# | `DiscountTypeSerializer`        | Cho dropdown loại giảm giá           |
# | `ApplyToSerializer`             | Cho dropdown đối tượng áp dụng       |


from rest_framework import serializers
from django.utils import timezone
from ..models.voucher import Voucher, VoucherUsage
from apps.core.serializers import UserSerializer
from apps.sales.serializers.order_serializer import OrderSerializer

# 🎯 Serializer cho lựa chọn loại giảm giá (phần trăm hoặc số tiền)
class DiscountTypeSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': str(instance[1])}

# 🎯 Serializer cho đối tượng áp dụng giảm giá
class ApplyToSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': str(instance[1])}
    
class VoucherSerializer(serializers.ModelSerializer):
    discount_type_display = serializers.CharField(source='get_discount_type_display', read_only=True)
    apply_to_display = serializers.CharField(source='get_apply_to_display', read_only=True)
    is_valid = serializers.SerializerMethodField()
    usage_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = [
            'id', 'code', 'name', 'description', 'discount_type', 'discount_type_display',
            'discount_value', 'apply_to', 'apply_to_display', 'min_order_value', 'max_discount_amount',
            'start_date', 'end_date', 'max_usage', 'current_usage', 'is_active',
            'allow_combined', 'for_first_time_buyers', 'for_organic_products',
            'is_valid', 'usage_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'current_usage', 'is_valid', 'usage_percentage', 'created_at', 'updated_at']

    def get_is_valid(self, obj):
        now = timezone.now()
        return (
            obj.is_active and
            obj.start_date <= now <= obj.end_date and
            (not obj.max_usage or obj.current_usage < obj.max_usage)
        )

    def get_usage_percentage(self, obj):
        return (obj.current_usage / obj.max_usage) * 100 if obj.max_usage else None

class VoucherCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = [
            'code', 'name', 'description', 'discount_type', 'discount_value',
            'apply_to', 'min_order_value', 'max_discount_amount', 'start_date',
            'end_date', 'max_usage', 'is_active', 'allow_combined',
            'for_first_time_buyers', 'for_organic_products'
        ]

    def validate(self, data):
        # ⛔ Kiểm tra giảm giá phần trăm
        if data.get('discount_type') == 'percentage' and data.get('discount_value') > 100:
            raise serializers.ValidationError({
                'discount_value': "Giảm giá phần trăm không thể lớn hơn 100%"
            })

        # ⛔ Kiểm tra ngày
        if data.get('start_date') and data.get('end_date') and data['start_date'] >= data['end_date']:
            raise serializers.ValidationError({
                'end_date': "Ngày kết thúc phải sau ngày bắt đầu"
            })

        return data

class VoucherUsageSerializer(serializers.ModelSerializer):
    voucher = VoucherSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = VoucherUsage
        fields = [
            'id', 'voucher', 'user', 'order',
            'discount_amount', 'applied_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'applied_at', 'created_at', 'updated_at']

class VoucherApplySerializer(serializers.Serializer):
    voucher_code = serializers.CharField(max_length=50)
    order_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)

    def validate_voucher_code(self, value):
        if not Voucher.objects.filter(code=value, is_active=True).exists():
            raise serializers.ValidationError("Voucher không tồn tại hoặc đã bị vô hiệu hóa")
        return value

class VoucherValidationSerializer(serializers.Serializer):
    is_valid = serializers.BooleanField()
    message = serializers.CharField()
    discount_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    voucher = VoucherSerializer(required=False)

