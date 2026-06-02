from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CustomerProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(label="Téléphone", max_length=30, required=False)
    address = forms.CharField(label="Adresse", widget=forms.Textarea(attrs={"rows": 2}), required=False)
    city = forms.CharField(label="Ville", max_length=80, required=False)
    postal_code = forms.CharField(label="Code postal", max_length=20, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "city",
            "postal_code",
            "password1",
            "password2",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ("phone", "address", "city", "postal_code")
