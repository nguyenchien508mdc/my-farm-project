from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class HarvestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.harvest"
    verbose_name = _("Thu hoạch")
