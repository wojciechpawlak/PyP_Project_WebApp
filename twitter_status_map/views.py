from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map
import twitter

from googlemaps import GoogleMaps
gmaps = GoogleMaps('AIzaSyD_7IvHQ55T3U1BphcJvHURbFlUpkcbErw')


def index(request):

    api = twitter.Api(
        consumer_key='Yu0TwUEvnPQW6tqmMmUhEw',
        consumer_secret='v4n7AXqj38sEgbuilRRGZhmrLr5IFZdCYjFtJ',
        access_token_key='757951074-zCFPCZ8hOFYaP7mZQnfZbM2vlAnLncZatfYKuqmw',
        access_token_secret='Yf9B7ufcks9fNFyVi54fW9mT85ml487HgmUcJSIepqI'
        )
    tweets=[]
    errors=[]
    user_search=0
    if 'q' in request.GET:
        if 'r' in request.GET and request.GET['r']:
            radius=request.GET['r']
        else:
            radius=25
        
        region=request.GET['q']
        user_search=1
        if region:
            lat, lng = gmaps.address_to_latlng(region)
            tw=api.GetSearch(geocode=(str(lat),str(lng),str(radius)+'km'),lang='')
            
            for i,t in enumerate(tw):
                tweets.append({'text':t.text,'user':t.user.AsDict()['screen_name']})
            
        else:
            errors.append('You entered an empty region.')
            region='Denmark, Anker Engelundsvej 1'
    else:
        region='Denmark, Anker Engelundsvej 1'
    
    cache_timeout = 900
    first_map = Map.objects.all()[0]
    context = {'first_map': region, 'cache_timeout': cache_timeout, 'errors':errors,'tweets':tweets,'user_search':user_search}
    return render(request, 'twitter_status_map/index.html', context)
