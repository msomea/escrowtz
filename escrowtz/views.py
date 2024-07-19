from django.shortcuts import render
from django.http import HttpResponseNotFound

def base_view(request):
    return render(request, 'escrowtz/base.html')