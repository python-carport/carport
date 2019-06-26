from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name = 'login'),
    path('appointment', views.appointment, name = 'appointment'),
    path('inquiry', views.inquiry, name = 'inquiry'),
]
