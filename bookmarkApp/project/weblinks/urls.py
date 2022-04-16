from django.urls import path
from . import views
from .views import (WeblinkCreateView,
                    WeblinkDetailView,
                    WeblinkUpdateView,
                    WeblinkDeleteView,
                    WeblinkListView)
 
urlpatterns = [   
    path('home/', views.weblink_home,name='weblink-home'),
    path('new/',WeblinkCreateView.as_view(),name='weblink-create'),
    path('detial/<int:pk>/',WeblinkDetailView.as_view(),name='weblink-detail'),
    path('update/<int:pk>/',WeblinkUpdateView.as_view(),name='weblink-update'),
    path('delete/<int:pk>/',WeblinkDeleteView.as_view(),name='weblink-delete'),
    path('list/',WeblinkListView.as_view() ,name='weblink-list'),
    
]