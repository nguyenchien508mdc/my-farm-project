from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.utils.text import slugify
from ..models.product import Product, ProductCategory, ProductImage, ProductReview


# Dịch vụ xử lý danh mục sản phẩm
class ProductCategoryService:
    @staticmethod
    def create_category(name, parent=None, description='', image=None, is_featured=False):
        cat = ProductCategory(name=name, parent=parent, description=description, image=image, is_featured=is_featured)
        cat.full_clean(); cat.save(); return cat

    @staticmethod
    def update_category(category_id, **kwargs):
        try:
            cat = ProductCategory.objects.get(id=category_id)
            for k, v in kwargs.items(): setattr(cat, k, v)
            cat.full_clean(); cat.save(); return cat
        except ProductCategory.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy danh mục")
        except Exception as e:
            raise ValidationError(str(e))

    @staticmethod
    def get_category_tree():
        return ProductCategory.objects.filter(parent=None).prefetch_related('children')

    @staticmethod
    def delete_category(category_id):
        try:
            cat = ProductCategory.objects.get(id=category_id)
            if cat.products.exists(): raise ValidationError("Danh mục còn sản phẩm")
            if cat.children.exists(): raise ValidationError("Danh mục còn danh mục con")
            cat.delete(); return True
        except ProductCategory.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy danh mục")

# Dịch vụ xử lý sản phẩm
class ProductService:
    @staticmethod
    @transaction.atomic
    def create_product(name, category, product_type='fresh', description='', price=0, unit='kg', stock=0,
                       is_available=True, is_organic=False, harvest_date=None, expiry_date=None, image=None, **kwargs):
        prod = Product(name=name, category=category, product_type=product_type, description=description,
                       price=price, unit=unit, stock=stock, is_available=is_available, is_organic=is_organic,
                       harvest_date=harvest_date, expiry_date=expiry_date, image=image, **kwargs)
        prod.full_clean(); prod.save(); return prod

    @staticmethod
    @transaction.atomic
    def update_product(product_id, **kwargs):
        try:
            prod = Product.objects.get(id=product_id)
            for k, v in kwargs.items(): setattr(prod, k, v)
            prod.full_clean(); prod.save(); return prod
        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy sản phẩm")
        except Exception as e:
            raise ValidationError(str(e))

    @staticmethod
    def get_available_products():
        return Product.objects.filter(is_available=True).select_related('category').prefetch_related('images')

    @staticmethod
    def get_featured_products():
        cats = ProductCategory.objects.filter(is_featured=True)
        return Product.objects.filter(category__in=cats, is_available=True).select_related('category').prefetch_related('images')[:12]

    @staticmethod
    def update_product_stock(product_id, quantity):
        try:
            with transaction.atomic():
                prod = Product.objects.select_for_update().get(id=product_id)
                prod.stock += quantity
                if prod.stock < 0: raise ValidationError("Tồn kho không đủ")
                prod.is_available = prod.stock > 0
                prod.save(); return prod
        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy sản phẩm")

    @staticmethod
    def delete_product(product_id):
        try:
            prod = Product.objects.get(id=product_id)
            prod.is_active = False
            prod.save(); return True
        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy sản phẩm")


# Dịch vụ xử lý hình ảnh sản phẩm
class ProductImageService:
    @staticmethod
    def add_product_image(product, image, alt_text='', is_default=False):
        if is_default:
            ProductImage.objects.filter(product=product, is_default=True).update(is_default=False)
        last = ProductImage.objects.filter(product=product).order_by('-order').first()
        order = (last.order + 1) if last else 0
        img = ProductImage(product=product, image=image, alt_text=alt_text, is_default=is_default, order=order)
        img.full_clean(); img.save(); return img

    @staticmethod
    def set_default_image(product_id, image_id):
        try:
            with transaction.atomic():
                ProductImage.objects.filter(product_id=product_id, is_default=True).update(is_default=False)
                img = ProductImage.objects.get(id=image_id, product_id=product_id)
                img.is_default = True; img.save(); return img
        except ProductImage.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy hình ảnh")

    @staticmethod
    def reorder_images(product_id, new_order):
        try:
            with transaction.atomic():
                imgs = ProductImage.objects.filter(product_id=product_id)
                id_map = {img.id: img for img in imgs}
                for order, img_id in enumerate(new_order):
                    if img_id in id_map:
                        id_map[img_id].order = order
                        id_map[img_id].save()
        except Exception as e:
            raise ValidationError(str(e))


# Dịch vụ xử lý đánh giá sản phẩm
class ProductReviewService:
    @staticmethod
    def create_review(product, user, rating, comment='', is_approved=True):
        try:
            review = ProductReview(product=product, user=user, rating=rating, comment=comment, is_approved=is_approved)
            review.full_clean(); review.save(); return review
        except Exception as e:
            raise ValidationError(str(e))

    @staticmethod
    def get_approved_reviews(product_id):
        return ProductReview.objects.filter(product_id=product_id, is_approved=True).select_related('user').order_by('-created_at')

    @staticmethod
    def get_average_rating(product_id):
        from django.db.models import Avg
        result = ProductReview.objects.filter(product_id=product_id, is_approved=True).aggregate(avg=Avg('rating'))
        return result['avg'] or 0

    @staticmethod
    def toggle_review_approval(review_id):
        try:
            review = ProductReview.objects.get(id=review_id)
            review.is_approved = not review.is_approved
            review.save(); return review
        except ProductReview.DoesNotExist:
            raise ObjectDoesNotExist("Không tìm thấy đánh giá")
