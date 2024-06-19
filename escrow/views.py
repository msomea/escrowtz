
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction

# Create your views here.
@login_required
def escrow_dashboard(request):
    return render(request, 'escrow/escrow_dashboard.html')

def create_escrow(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.sender = request.user
            transaction.save()
            return redirect('escrow:escrow_details', pk=transaction.pk)
    else:
        form = TransactionForm()
    return render(request, 'escrow/create_escrow.html', {'form':form})

def escrow_details(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'escrow/escrow_details.html', {'transaction':transaction})