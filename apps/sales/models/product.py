from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import BaseModel

class ProductCategory(BaseModel):
    name = models.CharField(_("Tên danh mục"), max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_("Danh mục cha"))
    description = models.TextField(_("Mô tả"), blank=True)
    image = models.ImageField(_("Hình ảnh"), upload_to='product_categories/', blank=True)
    is_featured = models.BooleanField(_("Nổi bật"), default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = _("Danh mục sản phẩm")
        verbose_name_plural = _("Danh mục sản phẩm")
        ordering = ['name']

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug, slug, counter = slugify(self.name), slugify(self.name), 1
        while ProductCategory.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
        return slug

class Product(BaseModel):
    PRODUCT_TYPES = (('fresh', _('Tươi sống')), ('processed', _('Đã chế biến')), ('packaged', _('Đóng gói sẵn')))

    name = models.CharField(_("Tên sản phẩm"), max_length=255)
    category = models.ForeignKey('sales.ProductCategory', on_delete=models.SET_NULL, null=True, related_name='products', verbose_name=_("Danh mục"))
    product_type = models.CharField(_("Loại sản phẩm"), max_length=20, choices=PRODUCT_TYPES, default='fresh')
    description = models.TextField(_("Mô tả"), blank=True)
    price = models.DecimalField(_("Giá bán"), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(_("Đơn vị"), max_length=20, default='kg')
    stock = models.PositiveIntegerField(_("Tồn kho"), default=0)
    is_available = models.BooleanField(_("Có sẵn"), default=True)
    is_organic = models.BooleanField(_("Hữu cơ"), default=False)
    harvest_date = models.DateField(_("Ngày thu hoạch"), null=True, blank=True)
    expiry_date = models.DateField(_("Hạn sử dụng"), null=True, blank=True)
    image = models.ImageField(_("Hình ảnh chính"), upload_to='products/', blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(_("Mã SKU"), max_length=50, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Sản phẩm")
        verbose_name_plural = _("Sản phẩm")
        ordering = ['-created_at']

    def __str__(self): return f"{self.name} ({self.sku})" if self.sku else self.name

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = self.generate_unique_slug()
        if not self.sku: self.sku = self.generate_sku()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug, slug, counter = slugify(self.name), slugify(self.name), 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
        return slug

    def generate_sku(self):
        prefix = "NONGTR" + timezone.now().strftime("%y%m")
        last_product = Product.objects.filter(sku__startswith=prefix).order_by('sku').last()
        last_seq = int(last_product.sku[-4:]) if last_product and last_product.sku and last_product.sku[-4:].isdigit() else 0
        return f"{prefix}{last_seq + 1:04d}"

class ProductImage(BaseModel):
    product = models.ForeignKey('sales.Product', on_delete=models.CASCADE, related_name='images', verbose_name=_("Sản phẩm"))
    image = models.ImageField(_("Hình ảnh"), upload_to='product_images/')
    alt_text = models.CharField(_("Văn bản thay thế"), max_length=255, blank=True)
    is_default = models.BooleanField(_("Hình mặc định"), default=False)
    order = models.PositiveIntegerField(_("Thứ tự hiển thị"), default=0)

    class Meta:
        verbose_name = _("Hình ảnh sản phẩm")
        verbose_name_plural = _("Hình ảnh sản phẩm")
        ordering = ['order']

    def __str__(self): return f"Hình của {self.product.name}"

class ProductReview(BaseModel):
    product = models.ForeignKey('sales.Product', on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Sản phẩm"))
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, verbose_name=_("Người dùng"))
    rating = models.IntegerField(_("Đánh giá (sao)"), validators=[MinValueValidator(1)], default=5)
    comment = models.TextField(_("Nhận xét"), blank=True)
    is_approved = models.BooleanField(_("Hiển thị công khai"), default=True)

    class Meta:
        verbose_name = _("Đánh giá sản phẩm")
        verbose_name_plural = _("Đánh giá sản phẩm")
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self): return f"Đánh giá {self.rating}⭐ cho {self.product.name} bởi {self.user}"
