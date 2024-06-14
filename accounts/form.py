from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10)
    
    class Meta:
        model = UserProfile
        field = ['phone_number']
        
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()
            user_profile.generate_otp()
        return user_profile


class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10, disabled=True)
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'first_name', 'last_name', 'user_name', 'email', 'address']
        
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['phone_number'].initial = self.instance.phone_number
        
    