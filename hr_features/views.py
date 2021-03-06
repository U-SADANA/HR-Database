from students.views import check_student
from django.shortcuts import render,redirect
from django.contrib import auth
from django.conf import settings
from accounts.models import User
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from .stud_filter import OrderFilter
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd


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
            branch=request.POST['branch']
            
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
            interview=interview,hrcount=hrcount,transport=transport,extra_comments=extra_comments,address=address,branch=branch)
            
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
            branch=request.POST['branch']

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
            hr.branch=branch

            messages.success(request,"HR Contact has been Edited Successfully!")
            hr.save()
            return redirect('show_hr_modal')
        else:
            hr=Hr.objects.filter(pk=id).first()
            return render(request,'hr_features/update.html',{"hr":hr})
    else:
        return redirect('student_login')

def delete_hr(request,id):
    
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
        name=request.user
        NC=0
        BC=0
        WN=0
        CNR=0 
        CP=0 
        CA=0 
        EAR=0 
        ED=0 
        EC=0
        count=0
        status_list={}
        for h in hrs:
            if h.status=="Not Called":
                NC=NC+1
            if h.status=="Blacklisted Contact":
                BC=BC+1
            if h.status=="Wrong Number":
                WN=WN+1
            if h.status=="Called/Not Reachable":
                CNR=CNR+1
            if h.status=="Called/Postponed":
                CP=CP+1
            if h.status=="Called/Accepted":
                CA=CA+1
            if h.status=="Emailed/Awaiting Response":
                EAR=EAR+1
            if h.status=="Emailed/Declined":
                ED=ED+1
            if h.status=="Emailed/Confirmed":
                EC=EC+1

            count=NC+BC+WN+CNR+CP+CA+EAR+ED+EC
        
        status_list={"NC":NC,"BC":BC,"WN":WN,"CNR":CNR,"CP":CP,"CA":CA,"EAR":EAR,"ED":ED,"EC":EC}
        
        hrs=Hr.objects.filter(added_by=request.user).order_by('-dtoc').all()
        return render(request,'hr_features/show_modal.html',{"hrs":hrs,"status_list":status_list,"count":count,"name":name})
    else:
        return redirect('student_login')

def Import_csv(request):               
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']   
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        excel_file = uploaded_file_url
        print(excel_file) 
        empexceldata = pd.read_excel("."+excel_file)
        print(type(empexceldata))
        dbframe = empexceldata
        count=0
        for dbframe in dbframe.itertuples():
            if not Hr.objects.filter(email=dbframe.email).exists() and not Hr.objects.filter(mobile=dbframe.mobile).exists():
                obj = Hr(added_by=request.user,fullname=str(dbframe.fullname),companyname=str(dbframe.companyname),email=dbframe.email,
                                            mobile=dbframe.mobile,status=str(dbframe.status), interview=str(dbframe.interview), hrcount=dbframe.hrcount, 
                                                dept=str(dbframe.dept), transport=str(dbframe.transport), extra_comments=str(dbframe.extra_comments),address=str(dbframe.address),
                                                internship=str(dbframe.internship),branch=str(dbframe.branch))
                if obj.status=='':
                    obj.status='Not Called'
                obj.save()
                count=count+1
                

        messages.success(request,str(count)+ " Contacts have been Imported Successfully!")   
            
        return redirect('show_hr_modal')    

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

def stud_stat(request):
    if request.user.is_authenticated and check_student(request.user):
        hrs=Hr.objects.filter(added_by=request.user).order_by('dtoc').all()
        name=request.user
        NC=0
        BC=0
        WN=0
        CNR=0 
        CP=0 
        CA=0 
        EAR=0 
        ED=0 
        EC=0
        count=0
        status_list={}
        for h in hrs:
            if h.status=="Not Called":
                NC=NC+1
            if h.status=="Blacklisted Contact":
                BC=BC+1
            if h.status=="Wrong Number":
                WN=WN+1
            if h.status=="Called/Not Reachable":
                CNR=CNR+1
            if h.status=="Called/Postponed":
                CP=CP+1
            if h.status=="Called/Accepted":
                CA=CA+1
            if h.status=="Emailed/Awaiting Response":
                EAR=EAR+1
            if h.status=="Emailed/Declined":
                ED=ED+1
            if h.status=="Emailed/Confirmed":
                EC=EC+1

            count=NC+BC+WN+CNR+CP+CA+EAR+ED+EC
        
        status_list={"NC":NC,"BC":BC,"WN":WN,"CNR":CNR,"CP":CP,"CA":CA,"EAR":EAR,"ED":ED,"EC":EC}
        return render(request,'hr_features/student_stat.html',{"status_list":status_list,"count":count,"name":name})
    else:
        return redirect('student_login')



def filter(request):
    if request.user.is_authenticated and check_student(request.user):
        hrs=Hr.objects.filter(added_by=request.user).order_by('-dtoc').all()
        myFilter=OrderFilter(request.GET, queryset=hrs)
        hrs=myFilter.qs

        return render(request,'hr_features/filter.html',{"hrs":hrs,"myFilter":myFilter})
    else:
        return redirect('student_login')