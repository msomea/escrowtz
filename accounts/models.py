from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    user_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True)
    address = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.user_name} {self.phone_number} {self.address} "