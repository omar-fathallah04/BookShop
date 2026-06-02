from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import CustomerProfile


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = getattr(user, "profile", None)
            if profile is None:
                profile = CustomerProfile.objects.create(user=user)
            profile.phone = form.cleaned_data.get("phone", "")
            profile.address = form.cleaned_data.get("address", "")
            profile.city = form.cleaned_data.get("city", "")
            profile.postal_code = form.cleaned_data.get("postal_code", "")
            profile.save()
            login(request, user)
            messages.success(request, "Compte cree avec succes.")
            return redirect("products:list")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    profile = getattr(request.user, "profile", None)
    if profile is None:
        profile = CustomerProfile.objects.create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil mis a jour.")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, "accounts/profile.html", {"user_form": user_form, "profile_form": profile_form})
