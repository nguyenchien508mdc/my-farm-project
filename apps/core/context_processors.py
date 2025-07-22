from .models import Configuration

def site_config(request):
    return {
        'site_config': {
            'name': Configuration.get_value('SITE_NAME', 'Nông trại Xanh'),
            'logo': Configuration.get_value('SITE_LOGO', '/static/images/logo.png'),
        }
    }