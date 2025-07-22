from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    # App URLs
    path('', include('apps.core.urls', namespace='core')),
    path('sales/', include('apps.sales.urls', namespace='sales')),
    path('farm/', include('apps.farm.urls', namespace='farm')),

    path('api/core/', include('apps.core.api.urls')),
    path('api/farm/', include('apps.farm.api.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
