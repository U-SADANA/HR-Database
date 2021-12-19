from django.db import models
from accounts.models import User

class TeamEDS(models.Model):
    team_name=models.CharField(max_length=25,unique=True,null=True)
    head_user=models.OneToOneField(User,on_delete=models.CASCADE)

class TeamMatch(models.Model):
    team_ed=models.ForeignKey(TeamEDS,on_delete=models.CASCADE)
    student_users=models.ForeignKey(User,on_delete=models.CASCADE)

    