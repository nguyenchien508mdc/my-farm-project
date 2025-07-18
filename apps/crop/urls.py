#apps\crop\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CropViewSet

app_name = 'crop'

router = DefaultRouter()
router.register(r'crops', CropViewSet, basename='crop')

urlpatterns = [
    path('', include(router.urls)),
]
