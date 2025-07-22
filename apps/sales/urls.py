# apps/sales/urls.py
from django.urls import path
from .views.product_view import ProductDetailView, CategoryProductListView, ProductListView


app_name = 'sales'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('danh-muc/<slug:slug>/', CategoryProductListView.as_view(), name='category_products'),
]