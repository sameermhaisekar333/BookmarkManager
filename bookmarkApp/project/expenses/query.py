from django.db.models import Sum
from django.db.models.functions import TruncMonth
from expenses.models import Expense 


def get_all_accounts(active):
    names = Expense.objects.values( 
                            "account"
                            ).filter(
                            created=active.request.user
                            ).order_by(
                            "account").distinct() 
    return names

def get_all_category_and_subcategory(active):
    names = Expense.objects.values(
                            "category",
                            "subcategory"
                            ).filter(
                            created=active.request.user,
                            ).order_by(
                            "category",
                            "subcategory"
                            ).distinct()               
    return names  

def get_data_for_day(active, date):
    all_day_psots =Expense.objects.filter(
                            created=active.request.user,
                            entry_date=date
                            ).order_by(
                            "-entry_date"
                            ).all()
    return all_day_psots   

def get_total_for_day(active, date):
    date_sum = Expense.objects.values(
                            "entry_date"
                            ).filter(
                            created=active.request.user,
                            entry_date=date
                            ).annotate( 
                            total=Sum("amount"))
    # print(date_sum)
    return date_sum


def get_total_info_for_day(active, date):
    info = Expense.objects.values(
                            "account", 
                            "category"
                            ).filter( 
                            created=active.request.user,
                            entry_date=date
                            ).annotate(
                            total=Sum("amount")
                            )
    # print(info)

    return info

def get_total_info_for_category(active,category):
    info = Expense.objects.annotate(
                            month=TruncMonth("entry_date"), 
                            ).values(
                            "month",
                            "account"
                            ).filter(
                            created=active.request.user,
                                category=category
                            ).annotate(
                            total=Sum("amount") 
                            )
    return(info)
                        
def get_total_for_category(active,category):
  
    category_sum = Expense.objects.values(
                            "category"
                            ).filter(
                            created=active.request.user,
                            category=category
                            ).annotate(
                            total=Sum("amount")
                            )
    return(category_sum)   
                 
def get_data_for_category(active,category):
    all_post_category = Expense.objects.filter(
                            created=active.request.user,
                            category=category
                            ).order_by(
                            "-entry_date" 
                            ).all()
    return all_post_category

def get_data_for_account(active,account):
    all_posts_account = Expense.objects.filter(
                            created=active.request.user,
                            account=account
                            ).order_by(
                            "-entry_date"
                            ).all()
    return all_posts_account                         
                            
def get_total_info_for_account(active,account): 
    info = Expense.objects.annotate(
                            month=TruncMonth("entry_date")
                            ).values(
                            "month",                
                            "category"
                            ).filter(
                            created=active.request.user,
                            account=account
                            ).annotate(
                            total=Sum("amount")) 
    return  info   
                      
def get_sum_for_account(active,account):
    account_sum = Expense.objects.values(
                            "account"
                            ).filter(
                            created=active.request.user,
                            account=account
                            ).annotate(
                            total=Sum("amount")  
                            )
    return account_sum  
                       
