from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, OTPVerificationForm, UserUpdateForm, LoginForm
from .models import UserProfile
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')
#User registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_profile = form.save()
            #OTP verification will resume later
            #user_profile.generate_otp()
            #return redirect('verify_otp',user_profile.id)
            login(request, user_profile.user)
            return redirect('update_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

#OTP verification
def verify_otp(request, user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            user_profile.is_verified = True
            user_profile.save()
            return redirect('profile_update')
    else:
        form = OTPVerificationForm(user_profile=user_profile)
    return render(request, 'accounts/verify_otp.html', {'form': form})

#Registered User login
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
#User log out
class CustomLogoutView(LogoutView):
    next_page = 'accounts:home'

#User profile update
@login_required
def profile_update(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_profile)
        if  form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=user_profile)
    return render(request, 'accounts/profile_update.html', {'form':form})

#other website render pages
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def login(request):
    return render(request, 'accounts/login.html')

def password_reset_confirm(request):
    return render(request, 'accounts/password_reset_confirm.html')

def password_reset(request):
    return render(request, 'accounts/password_reset.html')