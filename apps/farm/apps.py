from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class FarmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.farm"
    verbose_name = _("Quản lý Trang trại")
