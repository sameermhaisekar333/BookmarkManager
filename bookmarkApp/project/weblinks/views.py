from django.shortcuts import render
from .models import Weblink
from django.views.generic import ( 
                                ListView,
                                CreateView,
                                DetailView,
                                UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import (
                                LoginRequiredMixin,
                                UserPassesTestMixin)
from django.urls import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.

class WeblinkCreateView(
                        LoginRequiredMixin,
                        CreateView):
    model = Weblink                  
    fields = ['name','category','site'] 
    
    def form_valid(self, form):
        form.instance.created = self.request.user 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Weblink-Create'
        return context
    
    
class WeblinkDetailView(
                        LoginRequiredMixin, 
                        UserPassesTestMixin,
                        DetailView):
    model = Weblink                 #<app>/<model>_<viewtype>.html
                                   
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created:
            return True
        return False        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Weblink-Detail'
        return context         
                       
class WeblinkUpdateView( 
                        LoginRequiredMixin, 
                        UserPassesTestMixin,
                        UpdateView):
    model = Weblink                     #<app>/<model>_<viewtype>.html
    fields = ['name','category','site']
    
    def form_valid(self, form):
        form.instance.created = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created:
            return True
        return False  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Weblink-Update'
        return context

class WeblinkListView(
                    LoginRequiredMixin,
                    ListView): 
    model = Weblink     
    context_object_name = 'weblist'
    
    def get_queryset(self):
        qs = super().get_queryset()
        a = Weblink.objects.filter(created=self.request.user).order_by('category')
        
        return qs.filter(created=self.request.user).order_by('category')  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Weblink-List'
        return context

class WeblinkDeleteView(
                        LoginRequiredMixin, 
                        UserPassesTestMixin,
                        DeleteView):
    model = Weblink                 #<app>/<model>_<viewtype>.html       
    
    def test_func(self): 
        post = self.get_object()
        if self.request.user == post.created:
            return True
        return False   
      
    def get_success_url(self):
        return reverse("weblink-list") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Weblink-Delete'
        return context 
 
@login_required
def weblink_home(request):
  
    q=Weblink.objects.filter(created=request.user).values('category').distinct()  
    linked_content = []
    for content in q:
        linked_content.append(content['category'])
    #print (linked_content)
    query_cat = []
    for v in linked_content:
        liv = Weblink.objects.filter(category = v,created=request.user)
        query_cat.append(liv)
    #print(query_cat)   
 
    context = {
        'posts':zip(query_cat,linked_content),
        'title':'Weblink-Home',
        'link':linked_content,
    }   
    return render(request,
                'weblinks/weblink_home.html', 
                 context,    
                )
   