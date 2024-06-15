from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta

# Create your models here.
#User registaration function
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    user_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True)
    address = models.TextField(null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    
    # Generate OTP and send it to the usre phone number
    def generate_otp(self):
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OTP.objects.create(user=self.user, otp=otp_code, expires_at=datetime.now() + timedelta(minutes=5))
        # How to send the OTP to the user's phone number?

#Storing OTP
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        return datetime.now() < self.expires_at