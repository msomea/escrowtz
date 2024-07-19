from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
# new escrow transaction

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending','pending'),('completed','completed'),('canceled','canceled')], default='pending')

class Meta:
    indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
        ]   

def is_pending(self):
    return self.status == 'pending'

def is_completed(self):
    return self.status == 'completed'
 