from django.shortcuts import render
from students.views import check_student

from django.shortcuts import render,redirect
from django.contrib import auth
from django.conf import settings
from accounts.models import User
from .models import *
from django.http import JsonResponse
from django.contrib import messages


from .models import Hr
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def validate_email_hr(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': Hr.objects.filter(email=email).exists()
    }
    print(data)
    return JsonResponse(data)


def validate_phno(request):
    phno = request.GET.get('phone', None)
    data = {
        'is_taken': Hr.objects.filter(mobile=phno).exists()
    }
    print(data)
    return JsonResponse(data)


def add_hr(request):
    if request.user.is_authenticated and check_student(request.user):
        if request.method == 'POST':
            fullname=request.POST['fname']
            companyname=request.POST['cname']
            mobile=request.POST['phno']
            status=request.POST['status']
            interview=request.POST['interview']
            hrcount=0
            transport=request.POST['transport']
            
            if  request.POST['hrcount'] != "":
                hrcount=int(request.POST['hrcount'])

            email=""
            if 'email' in request.POST:
                email=request.POST['email']

            extra_comments=""
            if 'comments' in request.POST:
                extra_comments=request.POST['comments']

            address=""
            if 'address' in request.POST:
                address=request.POST['address']
           
            hr=Hr(added_by=request.user,fullname=fullname,companyname=companyname,email=email,mobile=mobile,status=status,
            interview=interview,hrcount=hrcount,transport=transport,extra_comments=extra_comments,address=address)
            
            dept=""
            if 'AUT' in request.POST:
                dept+='AUT '
            if 'BIO' in request.POST:
                dept+='BIO '
            if 'CHE' in request.POST:
                dept+='CHE '
            if 'CIVIL' in request.POST:
                dept+='CIVIL '
            if 'MECH' in request.POST:
                dept+='MECH '
            if 'EEE' in request.POST:
                dept+='EEE '
            if 'ECE' in request.POST:
                dept+='ECE '
            if 'CSE' in request.POST:
                dept+='CSE '
            if 'IT' in request.POST:
                dept+='IT '
            hr.dept=dept
            
            if 'internship' in request.POST:
                hr.internship=True

            hr.save()
            messages.success(request,"HR Contact Added Successfully!")
            return redirect('show_hr_modal')

        else:
            return render(request,'hr_features/add.html')
            
    else:
        return redirect('student_login')

def show_hr(request):
    if request.user.is_authenticated and check_student(request.user):
       hrs=Hr.objects.filter(added_by=request.user).order_by('dtoc').all()
       return render(request,'hr_features/show.html',{"hrs":hrs})
    else:
        return redirect('student_login')

def update_hr(request,id):
    if request.user.is_authenticated and check_student(request.user):
        if request.method == 'POST':
            hr=Hr.objects.filter(pk=id).first()
            fullname=request.POST['fname']
            companyname=request.POST['cname']
            mobile=request.POST['phno']
            status=request.POST['status']
            interview=request.POST['interview']
            hrcount=0
            transport=request.POST['transport']

            if  request.POST['hrcount'] != "":
                hrcount=int(request.POST['hrcount'])

            email=""
            if 'email' in request.POST:
                email=request.POST['email']

            extra_comments=""
            if 'comments' in request.POST:
                extra_comments=request.POST['comments']

            address=""
            if 'address' in request.POST:
                address=request.POST['address']
            
            dept=""
            if 'AUT' in request.POST:
                dept+='AUT '
            if 'BIO' in request.POST:
                dept+='BIO '
            if 'CHE' in request.POST:
                dept+='CHE '
            if 'CIVIL' in request.POST:
                dept+='CIVIL '
            if 'MECH' in request.POST:
                dept+='MECH '
            if 'EEE' in request.POST:
                dept+='EEE '
            if 'ECE' in request.POST:
                dept+='ECE '
            if 'CSE' in request.POST:
                dept+='CSE '
            if 'IT' in request.POST:
                dept+='IT '

            if 'internship' in request.POST:
                hr.internship=True
            
            hr.fullname=fullname
            hr.companyname=companyname
            hr.email=email
            hr.status=status
            hr.mobile=mobile
            hr.interview=interview
            hr.hrcount=hrcount
            hr.transport=transport
            hr.extra_comments=extra_comments
            hr.address=address
            hr.dept=dept

            messages.success(request,"HR Contact has been Edited Successfully!")
            hr.save()
            return redirect('show_hr_modal')
        else:
            hr=Hr.objects.filter(pk=id).first()
            return render(request,'hr_features/update.html',{"hr":hr})
    else:
        return redirect('student_login')

def delete_hr(request,id):
    context ={}
    if request.user.is_authenticated and check_student(request.user):
        hr=Hr.objects.filter(pk=id).first()
        hr.delete()
        return redirect('show_hr_modal')
    else:
        return redirect('student_login')
   

def hr_email(request):
    if request.user.is_authenticated and check_student(request.user):
        return render(request,'hr_features/email.html')
    else:
        return redirect('student_login')


def show_hr_modal(request):
    if request.user.is_authenticated and check_student(request.user):
       hrs=Hr.objects.filter(added_by=request.user).order_by('dtoc').all()
       return render(request,'hr_features/show_modal.html',{"hrs":hrs})
    else:
        return redirect('student_login')


def Import_csv(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']   
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                 
                obj = Hr.objects.create(added_by=request.user,fullname=dbframe.fullname,companyname=dbframe.companyname, email=dbframe.email,
                                                mobile=dbframe.mobile, status=dbframe.status, interview=dbframe.interview, hrcount=dbframe.hrcount, 
                                                dept=dbframe.dept, transport=dbframe.transport, extra_comments=dbframe.extra_comments,
                                                internship=dbframe.internship)
                print(type(obj))
                obj.save()
 
            return render(request, 'hr_features/Import_csv.html', {
                'uploaded_file_url': uploaded_file_url
            })    


    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'hr_features/Import_csv.html')


def faq(request):
    if request.user.is_authenticated and check_student(request.user):
       return render(request,'hr_features/faq.html')
    else:
        return redirect('student_login')

def pitch(request):
    if request.user.is_authenticated and check_student(request.user):
       return render(request,'hr_features/pitch.html')
    else:
        return redirect('student_login')
