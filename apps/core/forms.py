from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
    PasswordResetForm, SetPasswordForm
)
from .models import User, Configuration

# --- Form tạo người dùng (dùng cho admin) ---
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role')

# --- Form cập nhật người dùng (dùng cho admin) ---
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

# --- Form cấu hình hệ thống ---
class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = '__all__'
        widgets = {
            'value': forms.Textarea(attrs={'rows': 3}),
        }

# --- Form cập nhật hồ sơ người dùng ---
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 
            'email', 'phone_number',
            'date_of_birth', 'address',
            'profile_picture'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

# --- Form đăng ký người dùng ---
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# --- Form quên mật khẩu (Password Reset) ---
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )

# --- Form đặt lại mật khẩu (từ email) ---
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
