from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistationForm
from otp.models import OTP
from otp.views import send_otp_message

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            otp = OTP(user=user)
            otp.generate_otp()
            send_otp_sms(form.cleaned_data['phone_number'], otp.otp)
            request.session['user_id'] = user.id
            return redirect('otp:verify_otp')
        else:
            form = UserRegistationForm()
    return render(request, 'account/register.html', {'form': form})
        