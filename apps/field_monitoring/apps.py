from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class FieldMonitoringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.field_monitoring"
    verbose_name = _("Giám sát Ruộng")
