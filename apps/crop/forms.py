# apps/crop/forms.py
from django import forms
from .models import Crop, CropType
from django.utils.translation import gettext_lazy as _

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = [
            'farm',
            'crop_type',
            'variety',
            'status',
            'planting_date',
            'harvest_date',
            'area',
            'expected_yield',
            'actual_yield',
            'notes',
        ]
        labels = {
            'farm': _("Nông trại"),
            'crop_type': _("Loại cây"),
            'variety': _("Giống cây"),
            'status': _("Trạng thái"),
            'planting_date': _("Ngày trồng"),
            'harvest_date': _("Ngày thu hoạch"),
            'area': _("Diện tích (ha)"),
            'expected_yield': _("Năng suất dự kiến (tấn/ha)"),
            'actual_yield': _("Năng suất thực tế (tấn/ha)"),
            'notes': _("Ghi chú"),
        }
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date'}),
            'harvest_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area is not None and area <= 0:
            raise forms.ValidationError(_("Diện tích phải lớn hơn 0"))
        return area

    def clean(self):
        cleaned_data = super().clean()
        planting_date = cleaned_data.get('planting_date')
        harvest_date = cleaned_data.get('harvest_date')
        if planting_date and harvest_date and harvest_date < planting_date:
            raise forms.ValidationError(_("Ngày thu hoạch phải sau ngày trồng"))
        return cleaned_data
