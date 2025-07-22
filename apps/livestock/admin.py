from django.contrib import admin
from .models import AnimalType, Breed, Animal

@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'average_lifespan', 'maturity_age')
    search_fields = ('name', 'scientific_name')
    readonly_fields = ('id',)
    fieldsets = (
        ("Thông tin cơ bản", {
            'fields': ('name', 'scientific_name', 'description', 'image')
        }),
        ("Thông tin sinh học", {
            'fields': ('average_lifespan', 'maturity_age')
        }),
    )


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'origin')
    list_filter = ('animal_type',)
    search_fields = ('name', 'origin')
    autocomplete_fields = ['animal_type']
    readonly_fields = ('id',)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'identification_number', 'breed', 'gender', 'farm',
        'birth_date', 'acquisition_date', 'status'
    )
    list_filter = ('gender', 'status', 'farm', 'breed__animal_type')
    search_fields = ('identification_number', 'breed__name', 'acquisition_source')
    date_hierarchy = 'acquisition_date'
    autocomplete_fields = ['breed', 'farm', 'mother']
    readonly_fields = ('id',)
    fieldsets = (
        ("Thông tin cơ bản", {
            'fields': ('identification_number', 'gender', 'status')
        }),
        ("Thông tin giống & nông trại", {
            'fields': ('breed', 'farm', 'mother')
        }),
        ("Ngày tháng & nguồn gốc", {
            'fields': ('birth_date', 'acquisition_date', 'acquisition_source')
        }),
        ("Ghi chú", {
            'classes': ('collapse',),
            'fields': ('notes',)
        }),
    )
