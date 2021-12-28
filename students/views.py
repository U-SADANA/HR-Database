from django.shortcuts import render,redirect
from django.contrib import auth
from django.conf import settings
from accounts.models import User


def check_student(user):
    if user.user_type == 'VOLUNTEER':
        return True
    else:
	    return False


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']
        user = auth.authenticate(username=email,password=password)
        if user is not None :
            if user.user_type=='VOLUNTEER':
                auth.login(request,user,backend=None)
                return redirect('show_hr_modal')
            else:
                return redirect('teams_eds_login')
        else:
            return redirect('students_login')
    else:
        return render(request,'students/login.html')

def change_password(request):
    if request.user.is_authenticated and check_student(request.user):
        if request.method == 'POST':
            oldpwd = request.POST['pwd']
            newpwd = request.POST['npwd']
            user = auth.authenticate(username=request.user.email,password=oldpwd)
            if user is not None:
                user=User.objects.filter(email=request.user.email).first()
                user.set_password(newpwd)
                user.save()
                auth.logout(request)
                return redirect('students_login')
            
            else:
                 return redirect('students_change_password')
        else:
            return render(request,'students/changepassword.html')
    else:
        return redirect('students_login')


