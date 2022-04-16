from django import forms 
from .models import Expense
from django.contrib.auth.mixins import (
                            LoginRequiredMixin,
                            UserPassesTestMixin) 
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import (
                            CreateView,
                            ListView,
                            DetailView,
                            DeleteView,
                            UpdateView,
)


import plotly 
import plotly.express as px 
from django_pandas.io import read_frame, pd
import json
 
from .query import (
            get_all_accounts,
            get_all_category_and_subcategory,
            get_data_for_day,
            get_total_for_day,
            get_total_info_for_day,
            get_total_info_for_category,
            get_total_for_category,
            get_data_for_category,
            get_data_for_account,
            get_total_info_for_account,
            get_sum_for_account
)




# Create your views here.


class DateInput(forms.DateInput):
    input_type = "date"


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ["account", 
                  "category",
                  "subcategory",
                  "amount", 
                  "entry_date"]
        widgets = {
            "entry_date": DateInput(),
        }


class ExpenseCreateView(
                    LoginRequiredMixin,
                    SuccessMessageMixin, 
                    CreateView):
    model = Expense  # <expenses>/expense_form.html
    form_class = ExpenseForm 
    template_name = "expenses/expense_form.html"
    
    def form_valid(self, form):
        form.instance.created = self.request.user
        messages.success(self.request, f"Expense created successfully")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        accounts = get_all_accounts(active =self) 
        categories = get_all_category_and_subcategory(active= self)  
     
        context["accounts"] = accounts
        context["categories"] = categories   
        context["title"] = "Expense-Create"    

        return context


class ExpenseDetailView(
                    LoginRequiredMixin,
                    UserPassesTestMixin,
                    DetailView):
    model = Expense   # <expenses>/<expense>_<detail>.html
 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense-Detail" 
        return context

class ExpenseUpdateView(
                    LoginRequiredMixin, 
                    UserPassesTestMixin, 
                    UpdateView): 
    model = Expense
    form_class = ExpenseForm 
    template = "expenses/expense_form.html" 

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        accounts = get_all_accounts(active=self)
        
        categories = get_all_category_and_subcategory(active= self) 
    
        context["accounts"] = accounts
        context["categories"] = categories
        context["title"] = "Expense-Update" 

        return context

class ExpenseDeleteView(
                    LoginRequiredMixin, 
                    UserPassesTestMixin,
                    SuccessMessageMixin, 
                    DeleteView):
    model = Expense  # <app>/<model>_<viewtype>.html
    success_message = "deleted successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created:
            return True
        return False

    def get_success_url(self):
        return reverse("Expense-home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense-Delete" 
        return context


class ExpenseListView(
                LoginRequiredMixin, 
                ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    
    def get_queryset(self):
        return Expense.objects.filter(
            created=self.request.user).order_by("-entry_date")

    context_object_name = "posts"
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense-List" 
        return context


class ExpenseAccountListView(
                        LoginRequiredMixin,
                        ListView):
    model = Expense 
    template_name = "expenses/accounts.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.kwargs["account"]
        # print(account)
        account_sum = get_sum_for_account(
                                active= self,
                                account=account)
       
       
        all_posts = get_data_for_account(
                                active=self,
                                account=account)
    
       

        info =  get_total_info_for_account(active=self,
                                        account=account)
        
        chart_data = read_frame(info)
        # print(chart_data)

        chart_data["year_month"] = pd.to_datetime(chart_data["month"]).dt.to_period("M")

        #print(chart_data)

        chart_account = px.bar(
                            data_frame=chart_data,
                            x=chart_data.category,
                            y=chart_data.total, 
                            title=f"Account <b>{account}</b>",
                            text_auto=True,
                            color=chart_data.year_month,
                            template="plotly_dark",                            

                             )
        chart = json.dumps( 
                        chart_account, 
                        cls=plotly.utils.PlotlyJSONEncoder
                        )

        
        context["posts"] = all_posts 
        context["sum"] = account_sum 
        context["account_chart"] = chart
        context['title'] ='Expense-Account'
        context['value'] = f'Account {account}'

        return context


class ExpenseCategoryListView(
                        LoginRequiredMixin,
                        ListView):
    model = Expense
    template_name = "expenses/category.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs["category"]
        # print(category) 
        category_sum = get_total_for_category(
                            active=self,
                            category=category)

        

        all_posts = get_data_for_category(
                            active=self,
                            category=category)
       
        
       
        
        info =  get_total_info_for_category(
                            active=self,
                            category=category)
                                
       
        chart_data = read_frame(info)
        # print(chart_data)

        chart_data["year_month"] = pd.to_datetime(chart_data["month"]).dt.to_period("M")
        # print(chart_data)

        category_chart = px.bar(
                            data_frame=chart_data,
                            x=chart_data.account,
                            y=chart_data.total,
                            title=f"Category <b>{category}</b>",
                            text_auto=True,
                            color=chart_data.year_month,
                            template="plotly_dark" 
                            )
        chart = json.dumps(
                            category_chart,
                            cls=plotly.utils.PlotlyJSONEncoder 
                            )
        context["posts"] = all_posts
        context["category_chart"] = chart
        context['title']= 'Expense-Category'
        context['value'] = f'Category {category}'
        context["sum"] = category_sum
        return context 

  


class ExpenseDateListView(
                    LoginRequiredMixin,
                    ListView):
    model = Expense
     
    template_name = "expenses/date.html" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dates = self.kwargs["date"]
        #print(dates)
        date_sum = get_total_for_day( 
                            active=self, 
                            date=dates)
      
    
        all_posts = get_data_for_day(
                            active=self, 
                            date=dates) 
        
       
        info = get_total_info_for_day(
                        active=self,
                        date=dates)
         
        chart_data = read_frame(info)
        # print(data)
        date_chart = px.bar(
                            data_frame=chart_data,
                            x=chart_data.account,
                            y=chart_data.total,
                            title=f"Date <b>{dates}</b>",
                            text_auto=True,
                            color=chart_data.category ,
                            template="plotly_dark"
                            )
        chart = json.dumps(
                            date_chart,
                            cls=plotly.utils.PlotlyJSONEncoder
                            )
 
        context["date_chart"] = chart
        context["sum"] = date_sum
        context["posts"] = all_posts 
        context['value'] = f'Date {dates}'  
        context['title'] ='Expense-Date'  
        
        return context
  

                 

                                                    
