from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('darshboard/', views.user_dashboard, name='darshboard'),
    path('login/', views.login, name='login'),
    path('verify_otp/<int:user_profile_id>/', views.verify_otp, name='verify_otp'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('register/', views.register, name='register'),
]
