from django.db import models
from django.contrib.auth.models import User
import random, string
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    user_name = models.CharField(max_length=60, unique=True)
    otp = models.CharField(max_length=6, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone_number} {self.user_name} {self.email} {self.address} {self.created_at} {self.otp} {self.is_verified}'

def generate_otp():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class OTP(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f'{self.otp} {self.created_at} {self.expires_at}'

@receiver(post_save, sender=UserProfile)
def send_otp(sender, instance, created, **kwargs):
    if created:
        otp_code = generate_otp()
        instance.otp = otp_code
        instance.save()
        OTP.objects.create(user_profile=instance, otp=otp_code, expires_at=timezone.now() + timedelta(minutes=5))
