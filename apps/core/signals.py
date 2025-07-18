#apps\core\signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Configuration

User = get_user_model()

@receiver(pre_save, sender=User)
def set_superuser_status(sender, instance, **kwargs):
    """Tự động set is_staff và is_superuser khi role là admin"""
    if instance.role == 'admin':
        instance.is_staff = True
        instance.is_superuser = True
    else:
        instance.is_staff = False
        instance.is_superuser = False

@receiver(pre_save, sender=Configuration)
def log_config_change(sender, instance, **kwargs):
    """Ghi log khi cấu hình thay đổi"""
    if instance.pk:
        original = Configuration.objects.get(pk=instance.pk)
        if original.value != instance.value:
            # Gửi thông báo hoặc ghi log thay đổi
            pass