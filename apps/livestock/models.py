# apps/livestock/models.py
from django.db import models
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _

class AnimalType(BaseModel):
    name = models.CharField(_("Loại vật nuôi"), max_length=100)
    scientific_name = models.CharField(_("Tên khoa học"), max_length=100, blank=True)
    description = models.TextField(_("Mô tả"), blank=True)
    average_lifespan = models.PositiveIntegerField(_("Tuổi thọ trung bình (năm)"))
    maturity_age = models.PositiveIntegerField(_("Tuổi trưởng thành (tháng)"))
    image = models.ImageField(_("Hình ảnh"), upload_to='animal_types/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Loại vật nuôi")
        verbose_name_plural = _("Loại vật nuôi")

class Breed(BaseModel):
    animal_type = models.ForeignKey('livestock.AnimalType', on_delete=models.CASCADE, related_name='breeds')
    name = models.CharField(_("Giống"), max_length=100)
    origin = models.CharField(_("Nguồn gốc"), max_length=100, blank=True)
    characteristics = models.TextField(_("Đặc điểm"), blank=True)

    def __str__(self):
        return f"{self.animal_type.name} - {self.name}"

    class Meta:
        verbose_name = _("Giống vật nuôi")
        verbose_name_plural = _("Giống vật nuôi")

class Animal(BaseModel):
    GENDER_CHOICES = [
        ('male', 'Đực'),
        ('female', 'Cái'),
    ]

    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='animals')
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='animals')
    identification_number = models.CharField(_("Số hiệu"), max_length=50, unique=True)
    gender = models.CharField(_("Giới tính"), max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField(_("Ngày sinh"), null=True, blank=True)
    acquisition_date = models.DateField(_("Ngày nhập về"))
    acquisition_source = models.CharField(_("Nguồn gốc"), max_length=100)
    status = models.CharField(_("Tình trạng"), max_length=100, default='healthy')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    notes = models.TextField(_("Ghi chú"), blank=True)

    def __str__(self):
        return f"{self.breed} - {self.identification_number}"

    class Meta:
        verbose_name = _("Vật nuôi")
        verbose_name_plural = _("Vật nuôi")