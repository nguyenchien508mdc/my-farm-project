from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User, Role, Configuration

# ✅ Hiển thị lựa chọn vai trò (dùng cho dropdown frontend)
class RoleSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': str(instance[1])}

# ✅ Hiển thị thông tin người dùng
class UserSerializer(serializers.ModelSerializer):
    farms = serializers.SerializerMethodField()
    current_farm = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'address', 'is_verified', 'date_of_birth',
            'profile_picture', 'role', 'role_display',
            'farms', 'current_farm', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'is_verified', 'date_joined', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def get_farms(self, obj):
        from apps.farm.serializers import FarmSerializer  
        return FarmSerializer(obj.farms.all(), many=True).data

    def get_current_farm(self, obj):
        from apps.farm.serializers import FarmSerializer  
        if obj.current_farm:
            return FarmSerializer(obj.current_farm).data
        return None

# ✅ Tạo mới người dùng
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'role'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Mật khẩu xác nhận không khớp."})
        return data

    def create(self, validated_data):
        # Loại bỏ password2 ra khỏi validated_data trước khi tạo user
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)  # Mã hoá mật khẩu
        user.save()
        return user


# ✅ Cập nhật thông tin người dùng
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'phone_number', 'address', 'date_of_birth',
            'profile_picture', 'role', 'current_farm'
        ]

    def validate_role(self, value):
        if value not in dict(Role.choices):
            raise serializers.ValidationError("Vai trò không hợp lệ.")
        return value

# ✅ Thay đổi mật khẩu
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password2 = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu cũ không đúng.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Mật khẩu mới không trùng khớp."})
        return attrs

# ✅ Cấu hình hệ thống (key-value)
class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['id', 'key', 'value', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_key(self, value):
        exists = Configuration.objects.filter(key=value)
        if self.instance:
            exists = exists.exclude(id=self.instance.id)
        if exists.exists():
            raise serializers.ValidationError("Key này đã tồn tại.")
        return value
