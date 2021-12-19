from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login,name='students_login'),
    path('change_password/',views.change_password,name='students_change_password'),
]