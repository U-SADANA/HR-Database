from django.urls import path
from . import views

urlpatterns = [
    path('add_hr/',views.add_hr,name='add_hr'),
    path('show_hr/',views.show_hr,name='show_hr'),
    path('update_hr/<int:id>',views.update_hr,name='update_hr'),
    path('delete_hr/<int:id>',views.delete_hr,name='delete_hr'), 
    path('validate_email_hr',views.validate_email_hr,name='validate_email_hr'), 
    path('validate_phno',views.validate_phno,name='validate_phno'), 
    path('hr_email',views.hr_email,name='hr_email'), 
    path('show_hr_modal/',views.show_hr_modal,name='show_hr_modal'),
    path('Import_csv/', views.Import_csv,name="Import_csv"),  
    path('faq/', views.faq,name="faq"),  
    path('pitch/', views.pitch,name="pitch"),  
    path('stud_stat/', views.stud_stat,name="stud_stat"),  
    path('filter/', views.filter,name="filter"),  
]
