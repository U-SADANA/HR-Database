from django.urls import path
from . import views
urlpatterns = [
    path('validate_email/',views.validate_email,name='validate_email'),
    path('logout/',views.logout,name='logout'),
    path('',views.home,name='home')
]