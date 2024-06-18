from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, OTPVerificationForm, UserUpdateForm, LoginForm
from .models import UserProfile, OTP
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.urls import reverse

def home(request):
    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user_profile = form.save()
                login(request, user_profile.user)
                return redirect('accounts:verify_otp', user_profile_id=user_profile.id)
            except IntegrityError:
                form.add_error('user_name', 'Username already exists. Please choose another one.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    otp = user_profile.otp
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            if otp == entered_otp and OTP.objects.filter(user_profile=user_profile, otp=otp).first().is_valid():
                user_profile.is_verified = True
                user_profile.save()
                return redirect('accounts:dashboard')
            else:
                form.add_error('otp', 'Invalid OTP or OTP has expired.')
    else:
        form = OTPVerificationForm(user_profile=user_profile)
    return render(request, 'accounts/verify_otp.html', {'otp': otp, 'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'

@login_required
def profile_update(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard')
    else:
        form = UserUpdateForm(instance=user_profile)
    return render(request, 'accounts/profile_update.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def password_reset_confirm(request):
    return render(request, 'accounts/password_reset_confirm.html')

def password_reset(request):
    return render(request, 'accounts/password_reset.html')
