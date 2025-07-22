from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LivestockConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.livestock"
    verbose_name = _("Chăn nuôi")
