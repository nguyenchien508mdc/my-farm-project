from rest_framework import serializers
from .models import Farm, FarmMembership, FarmDocument

# ✅ Hiển thị các lựa chọn kiểu nông trại
class FarmTypeSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': instance[1]}

# ✅ Serializer đơn giản chỉ lấy thông tin cơ bản của Farm (dùng nested tránh vòng lặp)
class SimpleFarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'name', 'slug', 'location', 'area', 'farm_type',]

# ✅ Serializer chính hiển thị thông tin chi tiết nông trại
class FarmSerializer(serializers.ModelSerializer):
    farm_type_display = serializers.CharField(source='get_farm_type_display', read_only=True)
    members_count = serializers.SerializerMethodField()
    active_members_count = serializers.SerializerMethodField()

    class Meta:
        model = Farm
        fields = [
            'id', 'name', 'slug', 'location', 'area',
            'farm_type', 'farm_type_display', 'description',
            'is_active', 'established_date', 'logo',
            'created_at', 'updated_at', 'members_count', 'active_members_count'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'members_count', 'active_members_count']

    def get_members_count(self, obj):
        return obj.farmmembership_set.count()

    def get_active_members_count(self, obj):
        return obj.farmmembership_set.filter(is_active=True).count()

# ✅ Tạo/Cập nhật nông trại
class FarmCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = [
            'name', 'location', 'area', 'farm_type',
            'description', 'is_active', 'established_date', 'logo'
        ]

    def validate_area(self, value):
        if value < 0:
            raise serializers.ValidationError("Diện tích không thể âm")
        return value

# ✅ Hiển thị các vai trò trong nông trại (dùng cho dropdown)
class FarmMembershipRoleSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': instance[1]}

# ✅ Hiển thị thành viên của nông trại
class FarmMembershipSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = FarmMembership
        fields = [
            'id', 'farm', 'user', 'role', 'role_display',
            'joined_date', 'is_active', 'can_approve', 'created_at', 'updated_at'
        ]

    def get_user(self, obj):
        from apps.core.serializers import UserSerializer  
        return UserSerializer(obj.user).data

    def get_farm(self, obj):
        farm = obj.farm
        return {
            "id": farm.id,
            "name": farm.name,
            "slug": farm.slug,
            "location": farm.location if hasattr(farm, 'location') else None,
            "area": farm.area if hasattr(farm, 'area') else None,
            # thêm các trường khác nếu muốn
        }

# ✅ Tạo/Cập nhật vai trò thành viên trong nông trại
class FarmMembershipCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmMembership
        fields = ['farm', 'user', 'role', 'is_active', 'can_approve']

    def validate(self, data):
        # Kiểm tra nếu user đã là thành viên của nông trại
        if self.instance is None and FarmMembership.objects.filter(
            farm=data['farm'], user=data['user']
        ).exists():
            raise serializers.ValidationError("Người dùng đã là thành viên của nông trại này")
        return data

# ✅ Hiển thị các loại tài liệu
class FarmDocumentTypeSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'label': instance[1]}

# ✅ Hiển thị tài liệu chi tiết
class FarmDocumentSerializer(serializers.ModelSerializer):
    farm = SimpleFarmSerializer(read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = FarmDocument
        fields = [
            'id', 'farm', 'document_type', 'document_type_display',
            'title', 'file', 'file_url', 'issue_date', 'expiry_date',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'file_url']

    def get_file_url(self, obj):
        import os
        try:
            if obj.file and hasattr(obj.file, 'url'):
                path = obj.file.path
                if os.path.exists(path):  # kiểm tra tồn tại thật
                    return obj.file.url
            
        except Exception:
            return None
        return None



# ✅ Tạo/Cập nhật tài liệu
class FarmDocumentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmDocument
        fields = [
            'farm', 'document_type', 'title', 'file',
            'issue_date', 'expiry_date', 'description'
        ]

    def validate(self, attrs):
        issue_date = attrs.get('issue_date')
        expiry_date = attrs.get('expiry_date')

        # Nếu cả 2 ngày đều có thì kiểm tra
        if issue_date and expiry_date:
            if expiry_date < issue_date:
                raise serializers.ValidationError({
                    'expiry_date': "Ngày hết hạn phải sau ngày phát hành"
                })
        return attrs