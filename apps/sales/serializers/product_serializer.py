from rest_framework import serializers
from ..models.product import ProductCategory, Product, ProductImage, ProductReview
from apps.core.serializers import UserSerializer

# ----- Kiểu sản phẩm (ví dụ enum) -----
class ProductTypeSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        # Trả về dict gồm value và label từ tuple
        return {'value': instance[0], 'label': str(instance[1])}

# ----- Danh mục sản phẩm -----
class ProductCategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), required=False, allow_null=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent', 'description', 'image', 'is_featured', 'slug', 'children', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_children(self, obj):
        # Đệ quy lấy danh mục con
        return ProductCategorySerializer(obj.children.all(), many=True).data

# ----- Cây danh mục (chỉ lấy thông tin cơ bản) -----
class ProductCategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'image', 'children']

    def get_children(self, obj):
        return ProductCategoryTreeSerializer(obj.children.all(), many=True).data

# ----- Ảnh sản phẩm -----
class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'is_default', 'order']

    def get_image_url(self, obj):
        # Trả về url ảnh nếu có
        return obj.image.url if obj.image else None

# ----- Đánh giá sản phẩm -----
class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'comment', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_rating(self, value):
        # Đánh giá từ 1-5 sao
        if value < 1 or value > 5:
            raise serializers.ValidationError("Đánh giá phải từ 1 đến 5 sao")
        return value

# ----- Tạo đánh giá mới -----
class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['product', 'rating', 'comment']
        read_only_fields = ['product']

    def validate(self, data):
        user = self.context['request'].user
        product = self.context['product']
        # Kiểm tra user đã đánh giá sản phẩm chưa
        if ProductReview.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("Bạn đã đánh giá sản phẩm này rồi")
        return data

# ----- Sản phẩm chi tiết -----
class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'product_type', 'product_type_display', 'description', 'price', 'unit',
            'stock', 'is_available', 'is_organic', 'harvest_date', 'expiry_date', 'image', 'main_image', 'slug', 'sku',
            'images', 'reviews', 'average_rating', 'review_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'sku', 'created_at', 'updated_at', 'average_rating', 'review_count', 'main_image']

    def get_average_rating(self, obj):
        approved_reviews = obj.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            # Tính trung bình đánh giá
            return approved_reviews.aggregate(avg_rating=serializers.models.Avg('rating'))['avg_rating']
        return None

    def get_review_count(self, obj):
        # Đếm đánh giá đã duyệt
        return obj.reviews.filter(is_approved=True).count()

    def get_main_image(self, obj):
        # Ảnh mặc định hoặc ảnh đại diện sản phẩm
        default_img = obj.images.filter(is_default=True).first()
        if default_img:
            return default_img.image.url
        return obj.image.url if obj.image else None

# ----- Tạo hoặc cập nhật sản phẩm -----
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'product_type', 'description', 'price', 'unit', 'stock', 'is_available', 'is_organic', 'harvest_date', 'expiry_date', 'image']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Giá sản phẩm phải lớn hơn 0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Số lượng tồn kho không thể âm")
        return value

    def validate_expiry_date(self, value):
        harvest_date = self.initial_data.get('harvest_date')
        if value and harvest_date and value < harvest_date:
            raise serializers.ValidationError("Hạn sử dụng phải sau ngày thu hoạch")
        return value

# ----- Tạo ảnh sản phẩm -----
class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'alt_text', 'is_default', 'order']
        read_only_fields = ['product']

    def validate(self, data):
        # Nếu ảnh mới được đánh dấu mặc định, xóa mặc định các ảnh khác cùng sản phẩm
        if data.get('is_default'):
            ProductImage.objects.filter(product=self.context['product'], is_default=True).update(is_default=False)
        return data
