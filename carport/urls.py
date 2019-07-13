from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('appointment', views.appointment, name = 'appointment'),
    path('publish', views.publish, name = 'publish'),
    path('inquiry', views.inquiry, name = 'inquiry'),
    path('order_to', views.order_to, name = 'order_to'),
    path('order_from', views.order_from, name = 'order_from'),
    path('finish', views.finish, name = 'finish'),
    path('cancel', views.cancel, name = 'cancel'),
    path('negotiate', views.negotiate, name = 'negotiate'),
    path('inform', views.inform, name = 'inform'),
]
