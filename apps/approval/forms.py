# apps/approval/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

class ApprovalActionForm(forms.Form):
    notes = forms.CharField(
        label=_("Ghi chú"),
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': _("Nhập ghi chú phản hồi...")
        }),
        required=False
    )