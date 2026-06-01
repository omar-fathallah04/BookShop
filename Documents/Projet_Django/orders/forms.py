from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "address", "city", "phone")
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}
