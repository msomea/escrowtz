from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, OTP
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.utils import timezone
import random, string

def generate_otp():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

phone_regex = RegexValidator(regex=r'^\+\d{12}$', message="Phone number must be entered in the format: '+255123456789'.")

class UserRegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': '+255123456789'}),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )  
    password_confirm = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
    class Meta:
        model = UserProfile
        fields = ['user_name', 'phone_number', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data['user_name'], password=self.cleaned_data['password'])
        user_profile.user = user
        if commit:
            user_profile.save()
            otp_code = generate_otp()
            OTP.objects.create(user_profile=user_profile, otp=otp_code, expires_at=timezone.now() + timedelta(minutes=5))
        return user_profile

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'OTP'}),
    )

    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile')
        super().__init__(*args, **kwargs)

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        otp_instance = OTP.objects.filter(user_profile=self.user_profile, otp=otp).first()
        if not otp_instance or not otp_instance.is_valid():
            raise forms.ValidationError("Invalid or expired OTP")
        return otp

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'User Name'}),
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, disabled=True)
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    user_name = forms.CharField(
        required=True,
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'first_name', 'last_name', 'user_name', 'email', 'address', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        
        # Ensure username and phone number are not changed
        if 'user_name' in cleaned_data:
            cleaned_data.pop('user_name')
        if 'phone_number' in cleaned_data:
            cleaned_data.pop('phone_number')

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            user.save()
        if commit:
            user_profile.save()
        return user_profile
