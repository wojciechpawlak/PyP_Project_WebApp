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
            
            tw=removeReTweets(tw)
            
            for i,t in enumerate(tw):
                tweets.append({'text':t.text,'user':t.user.AsDict()['screen_name'],'datetime':t.AsDict()['created_at'],'image':t.user.AsDict()['profile_image_url']})
                texts.append(t.text)
        except GoogleMapsError:
            errors.append('Sorry, invalid region.')
            region='Denmark, Anker Engelundsvej 1'
            
    else:
        region='Denmark, Anker Engelundsvej 1'
    
    
    moodList=getRegionMood(texts)
    
    for i,t in enumerate(tweets):
        t['mood']=moodList[i]
        
        if moodList[i]=='None':
            t['moodColor']='black'
        elif moodList[i]==0:
            t['moodColor']='blue'
        elif moodList[i]<0:
            t['moodColor']='red'
        elif moodList>0:
            t['moodColor']='green'
    
    topicsTemp=getTopic(texts)[0:21]
    
    topics=[]
    for i,j in enumerate(topicsTemp):
        topics.append({'word':j[0],'freq':j[1],'mood':j[2]})
    
    moodListClean=cleanNoneMoods(moodList)
    moodListClean=np.array(moodListClean)
    sd=np.std(moodListClean)
    mean=np.mean(moodListClean)
    positives=sum(moodListClean>0)
    negatives=sum(moodListClean<0)
    neutrals=sum(moodListClean==0)
    NoMood=len(moodList)-len(moodListClean)
    
    moods={'sd':sd,'mean':mean,'positives':positives,'negatives':negatives,'neutrals':neutrals,'NoMood':NoMood}
    
    first_map = Map.objects.all()[0]
    context = {'first_map': region,  'errors':errors,'tweets':tweets,'user_search':user_search,'moodList':moodList,'moods':moods,'topics':topics}
    return render(request, 'twitter_status_map/index.html', context)
