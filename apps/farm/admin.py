from django.contrib import admin
from django.utils.html import format_html
from .models import Farm, FarmMembership, FarmDocument

class FarmMembershipInline(admin.TabularInline):
    model = FarmMembership
    extra = 0
    autocomplete_fields = ['user']
    fields = ('user', 'role', 'joined_date', 'is_active')
    readonly_fields = ('joined_date',)

class FarmDocumentInline(admin.TabularInline):
    model = FarmDocument
    extra = 0
    fields = ('document_type', 'title', 'file', 'expiry_date', 'description')
    readonly_fields = ('issue_date',)

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'area', 'farm_type', 'is_active', 'established_date', 'logo_preview')
    list_filter = ('farm_type', 'is_active')
    search_fields = ('name', 'location')
    readonly_fields = ('logo_preview',)
    inlines = [FarmMembershipInline, FarmDocumentInline]
    prepopulated_fields = {"slug": ("name",)}

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="80" style="border-radius: 4px; object-fit: cover;" />', obj.logo.url)
        return "Không có logo"
    logo_preview.short_description = "Xem logo"

@admin.register(FarmMembership)
class FarmMembershipAdmin(admin.ModelAdmin):
    list_display = ('farm', 'user', 'role', 'joined_date', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('farm__name', 'user__username')
    autocomplete_fields = ['farm', 'user']

@admin.register(FarmDocument)
class FarmDocumentAdmin(admin.ModelAdmin):
    list_display = ('farm', 'document_type', 'title', 'issue_date', 'expiry_date')
    list_filter = ('document_type', 'farm')
    search_fields = ('title', 'farm__name')
    autocomplete_fields = ['farm']
