from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class OperationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.operations"
    verbose_name = _("Vận hành")
