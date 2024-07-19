from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['receiver', 'amount', 'description']
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
        }

def clean_amount(self):
    amount = self.cleaned_data.get('amount')
    if amount <= 0:
        raise forms.ValidationError('Amount must be greater than zero.')
    return amount
