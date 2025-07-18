# apps/sales/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html
from django.urls import reverse

from .models.cart import Cart, CartItem
from .models.voucher import Voucher, VoucherUsage
from .models.product import ProductCategory, Product, ProductImage, ProductReview
from .models.order import Order, OrderItem

# ==================== CUSTOM ADMIN CLASSES ====================

class ReadOnlyAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

# ==================== INLINE ADMIN CLASSES ====================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "Ảnh sản phẩm"
    verbose_name_plural = "Thư viện ảnh"

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created_at']
    fields = ['user', 'rating', 'comment', 'created_at']
    can_delete = True
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        # Không cho thêm review trong admin inline (thường user review từ frontend)
        return False

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total_price']
    fields = ['quantity', 'price', 'total_price']
    def product_link(self, obj):
        url = reverse('admin:sales_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Sản phẩm'
    def total_price(self, obj):
        return f"{obj.total_price:,}₫"
    total_price.short_description = 'Thành tiền'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total_price']
    fields = ['quantity', 'price', 'discount_amount', 'total_price']
    def product_link(self, obj):
        url = reverse('admin:sales_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Sản phẩm'
    def total_price(self, obj):
        return f"{obj.total_price:,}₫"
    total_price.short_description = 'Thành tiền'

class VoucherUsageInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = VoucherUsage
    extra = 0
    readonly_fields = ['order_link', 'user', 'discount_amount', 'applied_at']
    fields = ['order_link', 'user', 'discount_amount', 'applied_at']
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:sales_order_change', args=[obj.order.id])
            return format_html('<a href="{}">Đơn #{}</a>', url, obj.order.id)
        return "-"
    order_link.short_description = 'Đơn hàng'

# ==================== RESOURCES ====================

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

# ==================== MAIN ADMIN ====================

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count', 'is_featured']
    list_filter = ['is_featured', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Số sản phẩm'

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['is_available', 'category']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ['name']}
    inlines = [ProductImageInline, ProductReviewInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'sku', 'category', 'description', 'image')
        }),
        ('Giá cả & Tồn kho', {
            'fields': ('price', 'stock', 'unit', 'is_available')
        }),
        ('Thông tin bổ sung', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item_count', 'total_price', 'created_at']
    list_select_related = ['user']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at']
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Số sản phẩm'
    def total_price(self, obj):
        return f"{obj.total:,}₫"
    total_price.short_description = 'Tổng tiền'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['id', 'customer__username', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('customer', 'status', 'created_at', 'updated_at')
        }),
        ('Thông tin thanh toán', {
            'fields': ('payment_method', 'payment_status', 'subtotal', 'discount_amount', 'shipping_fee', 'total')
        }),
        ('Thông tin giao hàng', {
            'fields': ('shipping_address', 'contact_phone', 'note', 'tracking_number')
        }),
    )
    actions = ['mark_as_paid', 'mark_as_shipped']
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payment_status=True)
        self.message_user(request, f"Đã đánh dấu {updated} đơn hàng đã thanh toán")
    mark_as_paid.short_description = "Đánh dấu đã thanh toán"
    def mark_as_shipped(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='shipped')
        self.message_user(request, f"Đã đánh dấu {updated} đơn hàng đã giao")
    mark_as_shipped.short_description = "Đánh dấu đã giao hàng"

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'discount_type', 'discount_value', 'is_active', 'usage_count', 'remaining_usage']
    list_filter = ['is_active', 'discount_type', 'apply_to']
    search_fields = ['code', 'name']
    filter_horizontal = ['products', 'categories']
    inlines = [VoucherUsageInline]
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('code', 'name', 'description', 'is_active')
        }),
        ('Chi tiết giảm giá', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount', 'apply_to', 'min_order_value')
        }),
        ('Phạm vi áp dụng', {
            'fields': ('products', 'categories')
        }),
        ('Thời hạn & Giới hạn', {
            'fields': ('start_date', 'end_date', 'max_usage', 'current_usage', 'allow_combined')
        }),
    )
    def usage_count(self, obj):
        return obj.usages.count()
    usage_count.short_description = 'Đã sử dụng'
    def remaining_usage(self, obj):
        if obj.max_usage:
            return obj.max_usage - obj.current_usage
        return "Không giới hạn"
    remaining_usage.short_description = 'Lượt dùng còn lại'

@admin.register(VoucherUsage)
class VoucherUsageAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ['voucher', 'order_link', 'user', 'discount_amount', 'applied_at']
    list_filter = ['voucher', 'applied_at']
    search_fields = ['voucher__code', 'user__username']
    readonly_fields = ['voucher', 'order', 'user', 'discount_amount', 'applied_at']
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:sales_order_change', args=[obj.order.id])
            return format_html('<a href="{}">Đơn #{}</a>', url, obj.order.id)
        return "-"
    order_link.short_description = 'Đơn hàng'
