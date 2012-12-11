from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map

from data_collector import DataCollector, RegionError
from twitter_status_map.util import *

import time
import numpy as np

def index(request):
    
    dc = DataCollector()
    
    tweets_to_show = []
    texts_to_analyze = []
    errors=[]
    
    user_search=0
    

    
    
    if 'q' in request.GET:
    
        if 'r' in request.GET and request.GET['r']:
            radius=request.GET['r']
        else:
            radius=25 # default radius
        
        region=request.GET['q']
        user_search=1
        try:
            tweets = dc.retrieve_tweets(region, radius)       
            
            for t in tweets:
                tweets_to_show.append({'text':t.text,'user':t.user.AsDict()['screen_name'],'datetime':t.AsDict()['created_at'],'image':t.user.AsDict()['profile_image_url']})
                texts_to_analyze.append(t.text)
        except RegionError as e:
            errors.append(e.value)
            region='Denmark, Anker Engelundsvej 1'
            
    else:
        region='Denmark, Anker Engelundsvej 1'
    
    
    moodList=getRegionMood(texts_to_analyze)
    
    for i,t in enumerate(tweets_to_show):
        t['mood']=moodList[i]
        
        if moodList[i]=='None':
            t['moodColor']='black'
        elif moodList[i]==0:
            t['moodColor']='blue'
        elif moodList[i]<0:
            t['moodColor']='red'
        elif moodList>0:
            t['moodColor']='green'
    
    topicsTemp=getTopic(texts_to_analyze)[0:21]
    
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
    
#    first_map = Map.objects.all()[0]
    
    context = {'first_map': region,  'errors':errors,'tweets':tweets,'user_search':user_search,'moodList':moodList,'moods':moods,'topics':topics}
    
    return render(request, 'twitter_status_map/index.html', context)
