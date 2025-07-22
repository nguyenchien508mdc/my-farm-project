# apps/sales/forms.py
from django import forms
from .models import Order, Product

class VoucherApplyForm(forms.Form):
    voucher_code = forms.CharField(
        label='Mã giảm giá',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập mã giảm giá',
            'class': 'form-control'
        })
    )

class OrderCancelForm(forms.Form):
    reason = forms.CharField(
        label='Lý do hủy đơn hàng',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Vui lòng nhập lý do hủy đơn hàng...'
        }),
        required=True
    )

class AddToCartForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_available=True),
        label="Sản phẩm"
    )
    quantity = forms.IntegerField(
    min_value=1,
    initial=1,
    label="Số lượng",
    widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'min': 1
    })
)

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'contact_phone',
            'note',
            'payment_method',
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'shipping_address': "Địa chỉ giao hàng",
            'contact_phone': "Số điện thoại",
            'note': "Ghi chú",
            'payment_method': "Phương thức thanh toán",
        }

    shipping_fee = forms.DecimalField(
        min_value=0,
        required=False,
        initial=0,
        label="Phí vận chuyển"
    )