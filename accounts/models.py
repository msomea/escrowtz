from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Manager):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)