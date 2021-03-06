from django.db import models
from accounts.models import User

INTERVIEW_CHOICE=(
    ('Offline','Offline'),
    ('Online','Online'),
    ('Undecided','Undecided'),
)


STATUS_CHOICE=(
    ('Not Called','Not Called'),
    ('Blacklisted Contact','Blacklisted Contact'),
    ('Wrong Number','Wrong Number'),
    ('Called/Not Reachable','Called/Not Reachable'),
    ('Called/Postponed','Called/Postponed'),
    ('Called/Accepted','Called/Accepted'),
    ('Emailed/Awaiting Response','Emailed/Awaiting Response'),
    ('Emailed/Declined','Emailed/Declined'),
    ('Emailed/Confirmed','Emailed/Confirmed'),
)

TRANSPORT_CHOICE=(
    ('Own Transport','Own Transport'),
    ('College Cab','College Cab'),
)

BRANCH_CHOICE=(
    ('Circuit Branches','Circuit Branches'),
    ('Non Circuit Branches','Non Circuit Branches'),
)
class Hr(models.Model):
    added_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    fullname=models.CharField( max_length=70)
    companyname=models.CharField( max_length=70)
    email=models.CharField( max_length=70,blank=True)
    mobile = models.CharField(max_length=10,unique=True)
    status=models.CharField(choices=STATUS_CHOICE,max_length=70)
    interview=models.CharField(choices=INTERVIEW_CHOICE,max_length=70)
    hrcount=models.PositiveIntegerField()
    dept=models.CharField(max_length=70)
    transport=models.CharField(choices=TRANSPORT_CHOICE,max_length=70)
    extra_comments=models.TextField()
    address=models.TextField(null=True)
    internship=models.BooleanField(default=False)
    dtoc=models.DateTimeField(auto_now_add=True,null=True)
    branch=models.CharField(choices=BRANCH_CHOICE,max_length=70,null=True)