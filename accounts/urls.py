from django.urls import path
from . import views
from .views import CustomLoginView, custom_logout

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('verify_otp/<int:user_profile_id>/', views.verify_otp, name='verify_otp'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('register/', views.register, name='register'),
]
