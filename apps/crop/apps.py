from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CropConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.crop"
    verbose_name = _("Quản lý Cây trồng")
