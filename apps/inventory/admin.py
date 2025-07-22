from django.contrib import admin
from .models import Supplier, InventoryItemCategory, InventoryItem, InventoryTransaction

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'is_active', 'rating')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_person', 'phone', 'email')
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('name', 'contact_person', 'phone', 'email', 'tax_code', 'is_active')
        }),
        ('Thông tin bổ sung', {
            'classes': ('collapse',),
            'fields': ('address', 'rating'),
        }),
    )


@admin.register(InventoryItemCategory)
class InventoryItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
    raw_id_fields = ('parent',)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'farm', 'category', 'supplier', 'current_stock', 'min_stock_level', 'unit')
    list_filter = ('item_type', 'unit', 'farm')
    search_fields = ('name',)
    autocomplete_fields = ['category', 'supplier', 'farm']
    readonly_fields = ('id',)
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'item_type', 'unit', 'farm', 'category', 'supplier')
        }),
        ('Tồn kho', {
            'fields': ('current_stock', 'min_stock_level')
        }),
        ('Chi tiết', {
            'classes': ('collapse',),
            'fields': ('description', 'storage_conditions')
        }),
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'item', 'quantity', 'date', 'farm', 'reference_number')
    list_filter = ('transaction_type', 'date', 'farm')
    search_fields = ('item__name', 'reference_number')
    autocomplete_fields = ['item', 'farm']
    readonly_fields = ('id',)
    date_hierarchy = 'date'
    fieldsets = (
        ('Thông tin giao dịch', {
            'fields': ('transaction_type', 'item', 'quantity', 'date', 'farm')
        }),
        ('Liên kết & ghi chú', {
            'classes': ('collapse',),
            'fields': ('reference_number', 'related_object_type', 'related_object_id', 'notes')
        }),
    )
