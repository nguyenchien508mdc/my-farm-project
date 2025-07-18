from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = _("Hệ thống lõi")

    def ready(self):
        import apps.core.signals