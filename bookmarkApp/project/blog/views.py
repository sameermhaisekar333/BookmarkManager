from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .ip_info import (    
                    home_ip,
                    country_detail,
                    create_map,
                    system_info,
                    user_info,
                    daily_trends,
                   )
# Create your views here. 
@login_required      
def home(request): 
    ipdata = home_ip()
  
    if not (ipdata['country'].isspace()):
        today_trend = daily_trends(ipdata['country'])
        #print(today_trend)

    context = {
        'title':'Home', 
        'trends':today_trend    
    }   
    #print(context['ip'])
    return render(request,
                'blog/home.html', 
                 context, 
                )
@login_required
def ip_home(request):
    ipdata = home_ip()
  
    if not (ipdata['country'].isspace()):
        country =country_detail(ipdata['country'])
        map =create_map(ipdata['latitude'],ipdata['longitude'])
        #sysdata =system_info() 
        userdata =user_info(request)
    
    context = {
        'title':'IP Detail',
        'ip':ipdata,
        'map':map,
        'country':country,
        'userdata':userdata,
        #'sysdata':sysdata
        
    }   
    
    return render(request,
                'blog/ip_detail.html',
                 context,
                )


