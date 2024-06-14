from django import forms
from .models import OTP

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)
    
    def _init_(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile')
        super().__init__(*args, **kwargs)
        
    def clean_otp(self):
        otp = self.cleaned_data['otp']
        otp_instance = OTP.objects.filter(user=self.user_profile.user, otp=otp).first()
        if not otp_instance or not otp_instance.is_valid():
            raise forms.ValidationError("Invalidy or Expired OTP")
        return otp