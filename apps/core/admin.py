#apps\core\admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Configuration

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone_number', 'role')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {
            'fields': (
                'first_name', 'last_name', 'email',
                'phone_number', 'date_of_birth',
                'profile_picture', 'address'
            )
        }),
        ('Phân quyền', {
            'fields': (
                'role', 'is_verified',
                'is_active', 'is_staff',
                'is_superuser', 'groups',
                'user_permissions'
            )
        }),
        ('Thông tin hệ thống', {'fields': ('last_login', 'date_joined')}),
        ('Liên kết nông trại', {'fields': ('current_farm',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email',
                'password1', 'password2',
                'role', 'is_verified'
            ),
        }),
    )


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'short_value', 'description')
    search_fields = ('key', 'description')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def short_value(self, obj):
        value_str = str(obj.value)
        return f"{value_str[:50]}..." if len(value_str) > 50 else value_str
    short_value.short_description = 'Giá trị'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
