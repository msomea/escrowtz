from django import forms
from .models import Transaction
from django.contrib.auth.models import User

class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount in Tsh',
                'step': '0.01'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Description',
                'row': 3
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

def clean_amount(self):
    amount = self.cleaned_data.get('amount')
    if amount <= 0:
        raise forms.ValidationError('Amount must be greater than zero.')
    return amount
