from django.urls import path
from . import views

app_name = 'escrow'

urlpatterns = [
    path('ecsrow_dashboard/', views.escrow_dashboard, name='escrow_dashboard'),
    
]