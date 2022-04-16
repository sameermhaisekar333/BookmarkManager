import folium
import requests
from pytrends.request import TrendReq
import time
import platform

def home_ip():
    #print("slept")
    time.sleep(3)
    response = requests.get('https://freegeoip.app/json/')
    #print("wokeup")
    if response.status_code == 200:
        data = response.json()
        
        #print(data["latitude"])
        # print(data["ip"])
        # print(data['longitude'])
        # print(data['country_name'])
        # print(data['city'])

        latitude = data["latitude"]
        longitude = data['longitude']
        ipdata = data["ip"]
        country = data['country_name']
        city = data['city']
        country_code =data['country_code']
        region_code =data['region_code']
        region_name =data['region_name']

    ip_response ={
            'latitude':latitude,
            'longitude':longitude,
            'ip':ipdata,
            'country':country,
            'city':city,
            'countrycode':country_code,
            'regioncode':region_code,
            'regionname':region_name 
            }
    return ip_response    

def country_detail(country_name):
    country = country_name.lower()
    url = f'https://restcountries.com/v3.1/name/{country}'
    #print(url)
    url_payload ={'fullText':"true"}
    res3 = requests.get(url,params=url_payload)
    #print(res3.url)
    data = res3.json()
    #print(data[0]['name']['common'])
    name =data[0]['name']['common']
    capital = data[0]['capital'][0]
    #print(data[0]['currencies']) 
    currency_symbol = data[0]['currencies']['INR']['symbol']
    currency_name = data[0]['currencies']['INR']['name']
    net = data[0]['tld'][0]
    time_zone = data[0]['timezones'][0]

    country_data ={
        'name':name,
        'capital': capital,
        'csymbol':currency_symbol,
        'cname':currency_name,
        'domian':net,
        'timezone':time_zone
      }
 
    return country_data


def daily_trends(country):
    country = country.replace(" ","_").lower()
    pytrend = TrendReq()
    a = pytrend.trending_searches(pn=country)  
    #print(a.head(15)) 
    #print(a[0])  
    data = a[0]
    #print(len(a))
    data_length = len(data)
    #print(data.values.tolist())
    data_list = data.values.tolist()
    link =[]
    for data in data_list:
        url =f'https://www.google.com/search?q={data}&sourceid=chrome&ie=UTF-8'
        #print(url) 
        link.append(url)
    return zip(data_list,link)


def create_map(latitude,longitude):
    
    #create a map
    map = folium.Map(zoom_start=4)  
    #create marker
    folium.Marker(location=[latitude,longitude],popup='you are here').add_to(map)
    #render to html
    map = map._repr_html_() 
    return map

def system_info():
  
    # print( f'("os.name       >>        " {os.name})' )
    # print("sys.platform      >>           ", sys.platform)
    # print("platform.system() >>           ", platform.system())
    # print("platform.release() >>          ", platform.release())
    # print("platform.version() >>          ", platform.version())
    # print("sysconfig.get_platform() >>     ", sysconfig.get_platform())
    # print("platform.machine()   >>        ", platform.machine())
    # print("platform.platform()  >>         ", platform.platform())
    # print("platform.node()      >>          ", platform.node())
    # print("platform.architecture() >>     ", platform.architecture())
    # print("platform.processor()  >>    ", platform.processor())
    platform_user = platform.system()
    platform_ver = platform.version()
    platform_processor =platform.processor() 
    sys_data= {
        'platform':platform_user ,
        'platformversion':platform_ver,
        'platformprocessor':platform_processor 
    }
   
    return sys_data
     
     
def user_info(request):
#   print(request.user_agent.is_mobile) # returns True
#   print(request.user_agent.is_tablet) # returns False
#   print(request.user_agent.is_touch_capable) # returns True
#   print(request.user_agent.is_pc) # returns False
#   print(request.user_agent.is_bot) # returns False

#   # Accessing user agent's browser attributes
#   print(request.user_agent.browser)  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
#   print(request.user_agent.browser.family)  # returns 'Mobile Safari'
#   print(request.user_agent.browser.version)  # returns (5, 1)
#   print(request.user_agent.browser.version_string )  # returns '5.1'

#   # Operating System properties
#   print(request.user_agent.os)  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
#   print(request.user_agent.os.family)  # returns 'iOS'
#   print(request.user_agent.os.version)  # returns (5, 1)
#   print(request.user_agent.os.version_string)  # returns '5.1'

#   # Device properties
#   print(request.user_agent.device ) # returns Device(family='iPhone')
#   print(request.user_agent.device.family)  # returns 'iPhone'
  
  browser =request.user_agent.browser.family
  browser_ver = request.user_agent.browser.version_string 
  #print(browser_ver)
  userinfo={
     'browser':browser,
     'browserver':browser_ver

    } 

  return userinfo

 