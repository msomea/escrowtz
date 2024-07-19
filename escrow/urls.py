from django.urls import path
from . import views

app_name = 'escrow'

urlpatterns = [
    path('ecsrow_dashboard/', views.escrow_dashboard, name='escrow_dashboard'),
    path('create_escrow/', views.create_escrow, name='create_escrow'),
    path('transaction/<int:pk>/', views.escrow_details, name='escrow_details' ),
    path('escrow_list/', views.escrow_list, name='escrow_list'),
]