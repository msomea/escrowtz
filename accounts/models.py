from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta

# Create your models here.
#User registaration function
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified =models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    user_name = models.CharField(max_length=60, unique=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone_number} {self.user_name} {self.email} {self.address} {self.created_at}'
    
    # Generate OTP and send it to the usre phone number
    def generate_otp(self):
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OTP.objects.create(user_profile=self, otp=otp, expires_at=datetime.now() + timedelta(minutes=5))
        return otp
        # To send the OTP to the user's phone number?
        # Implementation of the actual SMS sending logic here
        # For example, using Twilio
        # send_sms(self.phone_number, otp_code)

#Storing OTP
class OTP(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        return datetime.now() < self.expires_at
    
    def __str__(self):
        return f'{self.otp} {self.created_at} {self.expires_at}'