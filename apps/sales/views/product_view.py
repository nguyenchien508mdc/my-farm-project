from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from ..models.product import Product, ProductCategory, ProductReview
from ..services.product_service import ProductService, ProductCategoryService, ProductReviewService

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = ProductService.get_available_products()
        # Có thể mở rộng lọc theo query params, ví dụ:
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = ProductService.get_featured_products()
        context['categories'] = ProductCategoryService.get_category_tree()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['images'] = product.images.all().order_by('order')
        context['reviews'] = ProductReviewService.get_approved_reviews(product.id)
        context['average_rating'] = ProductReviewService.get_average_rating(product.id)

        # Thêm danh sách sản phẩm liên quan trong cùng danh mục, loại trừ chính nó
        related_products = Product.objects.filter(
            category=product.category,
            is_available=True
        ).exclude(id=product.id)[:4]
        context['related_products'] = related_products

        return context


class CategoryProductListView(ListView):
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, slug=self.kwargs['slug'])
        # Lấy sản phẩm trong danh mục hiện tại và cả danh mục con
        categories = [self.category] + list(self.category.children.all())
        return Product.objects.filter(category__in=categories, is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = ProductCategoryService.get_category_tree()
        return context
