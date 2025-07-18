# apps/field_monitoring/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _

class SoilMeasurement(BaseModel):
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='soil_measurements')
    location = models.CharField(_("Vị trí đo"), max_length=100, help_text="Ví dụ: Khu A, Lô 5")
    ph = models.FloatField(_("Độ pH"), validators=[MinValueValidator(0), MaxValueValidator(14)])
    organic_matter = models.FloatField(_("Chất hữu cơ (%)"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    nitrogen = models.FloatField(_("Nitơ (mg/kg)"), validators=[MinValueValidator(0)])
    phosphorus = models.FloatField(_("Phốt pho (mg/kg)"), validators=[MinValueValidator(0)])
    potassium = models.FloatField(_("Kali (mg/kg)"), validators=[MinValueValidator(0)])
    measurement_date = models.DateField(_("Ngày đo"))
    notes = models.TextField(_("Ghi chú"), blank=True)
    image = models.ImageField(_("Hình ảnh"), upload_to='soil_images/', blank=True)

    def __str__(self):
        return f"Soil at {self.location} on {self.measurement_date}"

    class Meta:
        verbose_name = _("Đo đạc đất")
        verbose_name_plural = _("Đo đạc đất")
        ordering = ['-measurement_date']

class WeatherRecord(BaseModel):
    farm = models.ForeignKey('farm.Farm', on_delete=models.CASCADE, related_name='weather_records')
    record_date = models.DateField(_("Ngày ghi nhận"))
    temperature = models.FloatField(_("Nhiệt độ (°C)"))
    humidity = models.FloatField(_("Độ ẩm (%)"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    rainfall = models.FloatField(_("Lượng mưa (mm)"), validators=[MinValueValidator(0)])
    wind_speed = models.FloatField(_("Tốc độ gió (km/h)"), validators=[MinValueValidator(0)])
    weather_condition = models.CharField(_("Tình trạng thời tiết"), max_length=100)
    sunshine_hours = models.FloatField(_("Số giờ nắng"), validators=[MinValueValidator(0), MaxValueValidator(24)], null=True, blank=True)

    def __str__(self):
        return f"Weather at {self.farm.name} on {self.record_date}"

    class Meta:
        verbose_name = _("Ghi nhận thời tiết")
        verbose_name_plural = _("Ghi nhận thời tiết")
        unique_together = ('farm', 'record_date')