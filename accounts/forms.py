from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, OTP

#Registration using phone number
class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10)
    
    class Meta:
        model = UserProfile
        fields = ['phone_number']
        
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()
            user_profile.generate_otp()
        return user_profile

#OTP verification form
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile')
        super().__init__(*args, **kwargs)

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        otp_instance = OTP.objects.filter(user=self.user_profile.user, otp=otp).first()
        if not otp_instance or not otp_instance.is_valid():
            raise forms.ValidationError("Invalid or expired OTP")
        return otp

#User profile details update
class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10, disabled=True)
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'first_name', 'last_name', 'user_name', 'email', 'address']
        
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['phone_number'].initial = self.instance.phone_number
        
    