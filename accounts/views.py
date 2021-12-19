from django.shortcuts import redirect, render
from .models import User
from django.http import JsonResponse
from django.contrib import auth


def home(request):
    return render(request,'accounts/home.html')


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)

def logout(request):
    auth.logout(request)
    return redirect('home')

