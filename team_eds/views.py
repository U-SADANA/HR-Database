from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.shortcuts import render,redirect
from django.contrib import auth
from django.conf import settings
from accounts.models import User
import team_eds
from .models import *
from hr_features.models import *
from .filters import OrderFilter
import xlwt


def check_team_ed(user):
    if user.user_type == 'TEAM_ED':
        return True
    else:
	    return False


def signup(request):
    if request.method == 'POST':
        user = User(fullname=request.POST['fname'],email=request.POST['email'],is_admin=True, user_type='TEAM_ED')
        user.set_password(request.POST['pwd'])
        user.save()
        team=TeamEDS(team_name=request.POST['tname'],head_user=user)
        team.save()
        auth.login(request,user,backend=None)
        return redirect('teams_eds_view_hrs')
    else:
        return render(request,'team_eds/signup.html')
        

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']
        user = auth.authenticate(username=email,password=password)
        if user is not None :
            if user.user_type=='TEAM_ED':
                auth.login(request,user,backend=None)
                return redirect('teams_eds_view_hrs')
            else:
                return redirect('students_login')
        else:
            return redirect('teams_eds_login')
    else:
        return render(request,'team_eds/login.html')


def add_student(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        if request.method == 'POST':
            user = User(fullname=request.POST['fname'],email=request.POST['email'],is_admin=True, user_type='VOLUNTEER')
            user.set_password(request.POST['pwd'])
            user.save()
            team=TeamEDS.objects.filter(head_user=request.user).first()
            team_match=TeamMatch(team_ed=team,student_users=user)
            team_match.save()
            return redirect('teams_eds_view_team')
        else:
            return render(request,'team_eds/add_student.html')
    else:
        return redirect('teams_eds_login')


def view_team(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        team=TeamEDS.objects.filter(head_user=request.user).first()
        students=TeamMatch.objects.all().filter(team_ed=team)
        return render(request,'team_eds/view_team.html',{"students":students})
    else:
        return redirect('teams_eds_login')


def view_hrs(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        team=TeamEDS.objects.filter(head_user=request.user).first()
        students=TeamMatch.objects.filter(team_ed=team).all()
        hrs=[]
        for student in students:
            hrs.append(Hr.objects.all().filter(added_by=student.student_users))

        return render(request,'team_eds/view_hrs.html',{"hrs":hrs})
    else:
        return redirect('teams_eds_login')

def teams_eds_view_allhrs(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        hrs=Hr.objects.order_by('added_by').all()
        
        myFilter=OrderFilter(request.GET, queryset=hrs)
        hrs=myFilter.qs

        return render(request,'team_eds/view_allhrs.html',{"hrs":hrs,"myFilter":myFilter})
    else:
        return redirect('teams_eds_login')

def progress(request,email):
    if request.user.is_authenticated and check_team_ed(request.user):
        student=User.objects.filter(email=email).first()
        hr_prog=Hr.objects.filter(added_by=student).all()
        return render(request,'team_eds/progress.html',{"hr_prog":hr_prog})
    else:
        return redirect('teams_eds_login')

def transport_filter(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        transport_filter=Hr.objects.all()
        return render(request,'team_eds/stat_transport.html',{"transport_filter":transport_filter})
    else:
        return redirect('teams_eds_login')


def changepassword(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        if request.method == 'POST':
            oldpwd = request.POST['pwd']
            newpwd = request.POST['npwd']
            user = auth.authenticate(username=request.user.email,password=oldpwd)
            if user is not None:
                user=User.objects.filter(email=request.user.email).first()
                user.set_password(newpwd)
                user.save()
                auth.logout(request)
                return redirect('teams_eds_login')
            
            else:
                 return redirect('changepassword')
        else:
            return render(request,'team_eds/changepassword.html')
    else:
        return redirect('teams_eds_login')


def file_load_view(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="HR_Database.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('HRs')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['HR Name', 'Company name', 'Email', 'Mobile','Status','Interview','Hr count','Department Preference','Transport Preference','Extra comments','Internship','address','branch']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = Hr.objects.all().values_list('fullname', 'companyname', 'email', 'mobile','status','interview','hrcount','dept','transport','extra_comments','internship','address','branch')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def statistics(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        hrs=Hr.objects.order_by('added_by').all()
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

        team=TeamEDS.objects.filter(head_user=request.user).first()
        students=TeamMatch.objects.filter(team_ed=team).all()
        hr_stud=[]
        status_list_team={}
        for student in students:
                hr_stud.append(Hr.objects.all().filter(added_by=student.student_users))
        teamcount=0
        TNC=0
        TBC=0
        TWN=0
        TCNR=0 
        TCP=0 
        TCA=0 
        TEAR=0 
        TED=0 
        TEC=0
        
        status_list_team={}
        for hrs in hr_stud:
            for h in hrs: 
                if h.status=="Not Called":
                    TNC=TNC+1
                if h.status=="Blacklisted Contact":
                    TBC=TBC+1
                if h.status=="Wrong Number":
                    TWN=TWN+1
                if h.status=="Called/Not Reachable":
                    TCNR=TCNR+1
                if h.status=="Called/Postponed":
                    TCP=TCP+1
                if h.status=="Called/Accepted":
                    TCA=TCA+1
                if h.status=="Emailed/Awaiting Response":
                    TEAR=TEAR+1
                if h.status=="Emailed/Declined":
                    TED=TED+1
                if h.status=="Emailed/Confirmed":
                    TEC=TEC+1

                teamcount=TNC+TBC+TWN+TCNR+TCP+TCA+TEAR+TED+TEC

                status_list_team={"TNC":TNC,"TBC":TBC,"TWN":TWN,"TCNR":TCNR,"TCP":TCP,"TCA":TCA,"TEAR":TEAR,"TED":TED,"TEC":TEC}
        return render(request,'team_eds/statistics.html',{"status_list":status_list,"count":count,"status_list_team":status_list_team,"teamcount":teamcount})
    else:
        return redirect('teams_eds_login')



def teams_eds_statistics(request,email):
    if request.user.is_authenticated and check_team_ed(request.user):
        student=User.objects.filter(email=email).first()
        hr_prog=Hr.objects.filter(added_by=student).all()
        name=student
        count=0
        NC=0
        BC=0
        WN=0
        CNR=0 
        CP=0 
        CA=0 
        EAR=0 
        ED=0 
        EC=0
        status_list={}
        for h in hr_prog:
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
        return render(request,'team_eds/student_statistics.html',{"status_list":status_list,"count":count,"name":name})
    else:
        return redirect('teams_eds_login')


