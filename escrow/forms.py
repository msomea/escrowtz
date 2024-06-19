from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['receiver', 'amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in Tsh'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Description' }),
        }