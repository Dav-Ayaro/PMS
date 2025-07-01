from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'Username and password are required.'})

        user = authenticate(request, username=username, password=password)
        if user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'otp.html', {'username': username})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def verify_otp(request):
    User = username
    if request.method == 'POST':
        username = request.POST.get('username')
        otp = request.POST.get('otp')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'otp.html', {'username': username, 'error': 'User not found'})

        if user.otp == otp:
            login(request, user)
            user.otp = None
            user.save()
            return redirect('dashboard')
        else:
            return render(request, 'otp.html', {'username': username, 'error': 'Invalid OTP'})

    return render(request, 'otp.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')