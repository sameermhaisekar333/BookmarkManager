from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.home,name='blog-home'), 
    path('ipdetail/',views.ip_home,name='blog-ipdetail'),
]