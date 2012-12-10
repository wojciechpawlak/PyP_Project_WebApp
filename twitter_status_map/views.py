from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map
import twitter

from googlemaps import GoogleMaps, GoogleMapsError
gmaps = GoogleMaps('AIzaSyD_7IvHQ55T3U1BphcJvHURbFlUpkcbErw')


def index(request):

    api = twitter.Api()
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
        try:
            lat, lng = gmaps.address_to_latlng(region.encode('utf8','ignore'))
            tw=api.GetSearch(geocode=(str(lat),str(lng),str(radius)+'km'),lang='')
            
            for i,t in enumerate(tw):
                tweets.append({'text':t.text,'user':t.user.AsDict()['screen_name']})
        except GoogleMapsError:
            errors.append('Sorry, invalid region.')
            region='Denmark, Anker Engelundsvej 1'
            
    else:
        region='Denmark, Anker Engelundsvej 1'
    
    
    first_map = Map.objects.all()[0]
    context = {'first_map': region,  'errors':errors,'tweets':tweets,'user_search':user_search}
    return render(request, 'twitter_status_map/index.html', context)
