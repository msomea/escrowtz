from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, OTP
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

#Registration using phone number
phone_regex = RegexValidator(regex=r'^\+\d{12}$', message="Phone number must be entered in the format: '+255123456789'.")

class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder':'+255123456789'}),
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
        fields = ['phone_number']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Password do not match')
        
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data['phone_number'], password=self.cleaned_data['password'])
        user_profile.user = user
        if commit:
            user_profile.save()
            user_profile.generate_otp()
        return user_profile

#OTP verification form
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'OTP'}),
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

#User login
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder':'User Name'}),
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    
#User profile details update
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
        fields = ['phone_number', 'first_name', 'last_name', 'user_name', 'email', 'address']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].initial = self.instance.phone_number
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Password do not match')
            
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user
        user.username = self.cleaned_data['user_name']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
            user.save()
        if commit:
            user_profile.save()
        return user_profile