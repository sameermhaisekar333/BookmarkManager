
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  
# Create your models here.

class Weblink(models.Model):
    name = models.CharField(max_length= 50)
    category = models.CharField(max_length=30)
    site = models.CharField(max_length=100)
    created = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Weblink('{self.name}','{self.category}','{self.site}','{self.created}')"

    def get_absolute_url(self):
        return reverse('weblink-detail',kwargs={'pk':self.pk})
    
    