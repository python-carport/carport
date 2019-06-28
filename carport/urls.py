from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name = 'login'),
    path('appointment', views.appointment, name = 'appointment'),
    path('inquiry', views.inquiry, name = 'inquiry'),
    path('order', views.order, name = 'order'),
    path('finish', views.finish, name = 'finish'),
    path('cancel', views.cancel, name = 'cancel'),

]
