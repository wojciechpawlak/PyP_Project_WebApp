'''
02820 Python Programming E12, DTU

PyP_Project_WebApp/twitter_status_map/views.py

Olavur Mortensen s103261, Wojciech Pawlak s091820

'''

from django.shortcuts import render


from twitter_status_map.data_collector import DataCollector, RegionError
from twitter_status_map.simple_sentiment_analyzer import SimpleSentimentAnalyzer

DC_OBJ = DataCollector()

TWEETS_TO_SHOW = []
TEXTS_TO_ANALYSE = []
ERRORS = []

def index(request):
    '''
    Rendering "index.html". Main page of site.
    '''
    
    
    
    region = 'Anker Engelunds Vej 1, Denmark' # default region
    radius = 15 # default radius
    user_search = 0 

    if 'q' not in request.GET: # first start of website
        context = {'first_map': region,
            'errors':ERRORS,
            'user_search':user_search}
        return render(request, 'twitter_status_map/index.html', context)
    elif 'q' in request.GET and request.GET['q'] != '': # correct behaviour
        region = request.GET['q']
        user_search = 1 
    elif 'q' in request.GET and request.GET['q'] == '': # empty textfield
        ERRORS.append('No region specified. Default region used.')


    if 'r' in request.GET and request.GET['r'] != '':
        radius = request.GET['r']
        
    try:
        tweets = DC_OBJ.retrieve_tweets(region, radius)       

    
    except RegionError as r_error:
        ERRORS.append(r_error.value)
        region = 'Anker Engelunds Vej 1, Denmark' 
        context = {'first_map': region,
            'errors': ERRORS,
            'user_search': user_search}
        return render(request, 'twitter_status_map/index.html', context)
            
           
    # extract fields from tweets to show and texts to analyze as lists
    for tweet in tweets:
        TWEETS_TO_SHOW.append({
                        'text': tweet.text,
                        'user': tweet.user.AsDict()['screen_name'],
                        'datetime': tweet.AsDict()['created_at'],
                        'image': tweet.user.AsDict()['profile_image_url']
                        })
        TEXTS_TO_ANALYSE.append(tweet.text)         
            
    ssa = SimpleSentimentAnalyzer()
    
    moods = ssa.get_region_moods(TEXTS_TO_ANALYSE)
    
    
    for idx, tweet in enumerate(TWEETS_TO_SHOW):
        tweet['mood'] = moods[idx]
        
        if moods[idx] == 'None':
            tweet['moodColor'] = 'black'
        elif moods[idx] == 0:
            tweet['moodColor'] = 'blue'
        elif moods[idx] < 0:
            tweet['moodColor'] = 'red'
        elif moods > 0:
            tweet['moodColor'] = 'green'
    
    mood_stats = ssa.prepare_mood_stats(moods)

    topics_temp = ssa.get_top_word_frequencies(TEXTS_TO_ANALYSE)[0:21]
    
    topics = []
    for topic in topics_temp:
        topics.append({'word':topic[0], 'freq':topic[1], 'mood':topic[2]})
    
#    first_map = Map.objects.all()[0]
    
    context = {
            'first_map': region,
            'errors': ERRORS,
            'tweets': TWEETS_TO_SHOW,
            'user_search': user_search,
            'moodList': moods, 
            'moods': mood_stats, 
            'topics': topics
            }
    
    return render(request, 'twitter_status_map/index.html', context)
