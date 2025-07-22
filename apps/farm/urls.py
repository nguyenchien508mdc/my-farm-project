# apps/farm/urls.py
from django.urls import path
from django.views.generic import TemplateView

app_name = 'farm'

urlpatterns = [
    path('', TemplateView.as_view(template_name='blank_app.html'), name='farm-list'),
    path('<slug:farm_slug>/members/', TemplateView.as_view(template_name='blank_app.html'), name='farm-membership'),
    path('<slug:farm_slug>/documents/', TemplateView.as_view(template_name='blank_app.html'), name='farm-documents'),
    path('<slug:farm_slug>/memberships/<str:username>/detail/',TemplateView.as_view(template_name='blank_app.html'),name='farm-membership-detail'),
]
