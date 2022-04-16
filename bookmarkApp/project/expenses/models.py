from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse  

# Create your models here.

class Expense(models.Model): 
    account = models.CharField(max_length= 25,blank=False)
    category = models.CharField(max_length=25,blank= False)
    subcategory = models.CharField(max_length=25,blank=True)
    amount = models.BigIntegerField(validators=[MinValueValidator(0.1)]) 
    entry_date = models.DateField()
    created = models.ForeignKey(User, on_delete=models.CASCADE) 
     

    def __str__(self):
        return f"Expense('{self.account}','{self.category}','{self.subcategory}','{self.amount}','{self.entry_date}','{self.created}')" 

    def get_absolute_url(self): 
        return reverse('Expense-detail',kwargs={'pk':self.pk})
    