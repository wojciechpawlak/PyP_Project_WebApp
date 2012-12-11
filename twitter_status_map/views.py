from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map
import twitter

from googlemaps import GoogleMaps, GoogleMapsError
gmaps = GoogleMaps('AIzaSyD_7IvHQ55T3U1BphcJvHURbFlUpkcbErw')

from twitter_status_map.util import *

import numpy as np
import time

def index(request):
    
    api = twitter.Api()
    tweets=[]
    errors=[]
    user_search=0
    texts=[]
    if 'q' in request.GET:
        if 'r' in request.GET and request.GET['r']:
            radius=request.GET['r']
        else:
            radius=25
        
        region=request.GET['q']
        user_search=1
        try:
            lat, lng = gmaps.address_to_latlng(region.encode('utf8','ignore'))
            tw1=api.GetSearch(geocode=(str(lat),str(lng),str(radius)+'km'),lang='en',per_page=100,page=1)
            tw1 = tw1 + api.GetSearch(geocode=(str(lat),str(lng),str(radius)+'km'),lang='en',per_page=100,page=2)
            tw1 = tw1 + api.GetSearch(geocode=(str(lat),str(lng),str(radius)+'km'),lang='en',per_page=100,page=3)
            
            tw2=api.GetSearch(term=region,lang='en',per_page=100, page=1)
            tw2=tw2 + api.GetSearch(term=region,lang='en',per_page=100, page=2)
            tw2=tw2 + api.GetSearch(term=region,lang='en',per_page=100, page=3)

            tw_list = tw1 + tw2
            tw_set = set(tw_list)
            tw_us = list(tw_set) 
            
            tw = sorted(tw_us, key=lambda t: time.strptime(t.created_at, "%a, %d %b %Y %H:%M:%S +0000"), reverse=True)
            
            for i,t in enumerate(tw):
                tweets.append({'text':t.text,'user':t.user.AsDict()['screen_name'],'datetime':t.AsDict()['created_at']})
                texts.append(t.text)
        except GoogleMapsError:
            errors.append('Sorry, invalid region.')
            region='Denmark, Anker Engelundsvej 1'
            
    else:
        region='Denmark, Anker Engelundsvej 1'
    
    moodList=getAreaMood(texts)
    
    moodList=np.array(moodList)
    sd=np.std(moodList)
    mean=np.mean(moodList)
    positives=sum(moodList>0)
    negatives=sum(moodList<0)
    neutrals=sum(moodList==0)
    
    moods={'sd':sd,'mean':mean,'positives':positives,'negatives':negatives,'neutrals':neutrals}
    
    first_map = Map.objects.all()[0]
    context = {'first_map': region,  'errors':errors,'tweets':tweets,'user_search':user_search,'moodList':moodList,'moods':moods}
    return render(request, 'twitter_status_map/index.html', context)
