from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map

from data_collector import DataCollector, RegionError
from simple_sentiment_analyzer import SimpleSentimentAnalyzer

def index(request):
    
    dc = DataCollector()
    
    tweets_to_show = []
    texts_to_analyze = []
    errors = []
    
    region = 'Anker Engelunds Vej 1, Denmark' # default region
    radius = 15 # default radius
    user_search = 0 

    if 'q' not in request.GET: # first start of website
        context = {'first_map': region,  'errors':errors, 'user_search':user_search}
        return render(request, 'twitter_status_map/index.html', context)
    elif 'q' in request.GET and request.GET['q'] != '': # correct behaviour
        region = request.GET['q']
        user_search=1 
    elif 'q' in request.GET and request.GET['q'] == '': # empty textfield
        errors.append('No region specified. Default region used.')


    if 'r' in request.GET and request.GET['r'] != '':
        radius = request.GET['r']
        
    try:
        tweets = dc.retrieve_tweets(region, radius)       

    
    except RegionError as e:
        errors.append(e.value)
        region='Anker Engelunds Vej 1, Denmark' 
        context = {'first_map': region,  'errors': errors, 'user_search': user_search}
        return render(request, 'twitter_status_map/index.html', context)
            
           
    # extract fields from tweets to show and texts to analyze as lists
    for t in tweets:
        tweets_to_show.append({
                        'text': t.text,
                        'user': t.user.AsDict()['screen_name'],
                        'datetime': t.AsDict()['created_at'],
                        'image': t.user.AsDict()['profile_image_url']
                        })
        texts_to_analyze.append(t.text)         
            
    ssa = SimpleSentimentAnalyzer()
    
    moods = ssa.get_region_moods(texts_to_analyze)
    
    
    for i,t in enumerate(tweets_to_show):
        t['mood']=moods[i]
        
        if moods[i]=='None':
            t['moodColor']='black'
        elif moods[i]==0:
            t['moodColor']='blue'
        elif moods[i]<0:
            t['moodColor']='red'
        elif moods>0:
            t['moodColor']='green'
    
    mood_stats = ssa.prepare_mood_stats(moods)

    topicsTemp = ssa.get_topic(texts_to_analyze)[0:21]
    
    topics=[]
    for i,j in enumerate(topicsTemp):
        topics.append({'word':j[0],'freq':j[1],'mood':j[2]})
    
#    first_map = Map.objects.all()[0]
    
    context = {
            'first_map': region,
            'errors': errors,
            'tweets': tweets_to_show,
            'user_search': user_search,
            'moodList': moods, 
            'moods': mood_stats, 
            'topics': topics
            }
    
    return render(request, 'twitter_status_map/index.html', context)
