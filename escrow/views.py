
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def escrow_dashboard(request):
    return render(request, 'escrow/escrow_dashboard.html')
