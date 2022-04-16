from django.urls import path
from . import views
from .views import (ExpenseCreateView,
                    ExpenseListView,
                    ExpenseDateListView,
                    ExpenseAccountListView,
                    ExpenseCategoryListView,
                    ExpenseDetailView,
                    ExpenseUpdateView,  
                    ExpenseDeleteView
                    ) 

urlpatterns = [   
    path('new/',ExpenseCreateView.as_view(),name='Expense-new'), 
    path('home/',ExpenseListView.as_view(),name='Expense-home'),
    path('update/<int:pk>/',ExpenseUpdateView.as_view(),name='Expense-update'),   
    path('detail/<int:pk>/',ExpenseDetailView.as_view(),name='Expense-detail'),  
    path('delete/<int:pk>/',ExpenseDeleteView.as_view(),name='Expense-delete'), 
    path('account/<str:account>/',ExpenseAccountListView.as_view(),name='Expense-account'),
    path('category/<str:category>/',ExpenseCategoryListView.as_view(),name='Expense-category'),
    path('date/<str:date>/',ExpenseDateListView.as_view(),name='Expense-date')      
]     