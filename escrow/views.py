
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction
from django.core.paginator import Paginator

# Create your views here.
@login_required
def escrow_dashboard(request):
    user = request.user
    previous_transactions = Transaction.objects.filter(receiver=user).exclude(status='pending')
    current_transactions = Transaction.objects.filter(receiver=user, status='pending')
    disputes = []  # Replace with actual dispute fetching if you have a Dispute model

    context = {
        'user': user,
        'previous_transactions': previous_transactions,
        'current_transactions': current_transactions,
        'disputes': disputes,
    }
    return render(request, 'escrow/escrow_dashboard.html', context)

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
    context = {
        'transaction': transaction,
    }
    return render(request, 'escrow/escrow_details.html', context)

def escrow_list(request):
    transactions_list = Transaction.objects.all()
    paginator = Paginator(transactions_list, 1)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'escrow/escrow_list.html', context)