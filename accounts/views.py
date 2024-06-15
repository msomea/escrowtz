from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, OTPVerificationForm, UserUpdateForm
from .models import UserProfile, OTP

# Create your views here.
#User registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_profile = form.save()
            user_profile.generate_otp()
            return redirect('verify_otp',user_profile.id)
        else:
            form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

#OTP verification
def verify_otp(request, user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            return redirect('profile_update')
    else:
        form = OTPVerificationForm(user_profile=user_profile)
    return render(request, 'accounts/verify_otp.html', {'form': form})

#User profile update
def profile_update(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_profile)
        if  form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = UserUpdateForm(instance=user_profile)
    return render(request, 'accounts/profile_update.html', {'form':form})

#other website render pages
def user_dashboard(request):
    return(request, 'accounts/dashboard.html')

def login(request):
    return(request, 'accounts/login.html')

def password_reset_confirm(request):
    return(request, 'accounts/password_reset_confirm.html')

def password_reset(request):
    return(request, 'accounts/password_reset.html')