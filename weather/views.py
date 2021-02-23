from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import requests
from .models import City

# Create your views here.
def index(request):
    msg = ''
    msg_class = ''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=409bb0a0ae63c510f8351794fac08963'

    if request.method == 'POST':
        name = request.POST['name']
        r = requests.get(url.format(name)).json()
        count = City.objects.filter(name = name).count()
        print(r)
        if r["cod"] == 200:
            city = City(name = name)
            city.save()
            msg = 'city saved succesfully...!!!'
            msg_class = 'alert-success'
        elif r['cod'] == '404':
            msg = "city doesn't exist...!!!"
            msg_class = 'alert-danger'
            print(r)
        elif count != 0:
            msg = "city already exist...!!!"
            msg_class = 'alert-danger'
   
    cities = City.objects.all()
    
    weather_data = []
    for i in cities:
        r = requests.get(url.format(i)).json()
        city_weather = {
            'city' : i.name,
            'temperature' : r['main']['temp'] ,
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'msg' : msg , 'msg_class' : msg_class}

    return render(request,'weather.html',context)

def delete(request,city):
    City.objects.filter(name = city).delete()
    return redirect('/')