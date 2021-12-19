from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login,name='teams_eds_login'),
    path('signup/',views.signup,name='teams_eds_signup'),
    path('add_student/',views.add_student,name='teams_eds_add_student'),
    path('view_team/',views.view_team,name='teams_eds_view_team'),
    path('view_hrs/',views.view_hrs,name='teams_eds_view_hrs'),
    path('progress/<str:email>',views.progress,name='teams_eds_progress'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('teams_eds_view_allhrs/',views.teams_eds_view_allhrs,name='teams_eds_view_allhrs'),

]