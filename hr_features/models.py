from django.db import models
from accounts.models import User

INTERVIEW_CHOICE=(
    ('Offline','Offline'),
    ('Online','Online'),
    ('Undecided','Undecided'),
)


STATUS_CHOICE=(
    ('Not Called','Not Called'),
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

class Hr(models.Model):
    added_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    fullname=models.CharField( max_length=70)
    companyname=models.CharField( max_length=70)
    email=models.CharField( max_length=70,unique=True)
    mobile = models.CharField(max_length=10,unique=True)
    status=models.CharField(choices=STATUS_CHOICE,max_length=70)
    interview=models.CharField(choices=INTERVIEW_CHOICE,max_length=70)
    hrcount=models.PositiveIntegerField()
    dept=models.CharField(max_length=70)
    transport=models.CharField(choices=TRANSPORT_CHOICE,max_length=70)
    extra_comments=models.TextField()


