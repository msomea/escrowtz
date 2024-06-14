from django.db import models
from django.contrib.auth.models import User
import random
from datetime import timedelta, datetime

# Create your models here.
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def generate_otp(self):
        self.opt=''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=5)
        self.save()
        
    def is_valid(self):
        return datetime.now() < self.expires_at