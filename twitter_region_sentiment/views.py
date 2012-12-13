'''
02820 Python Programming E12, DTU

PyP_Project_WebApp/twitter_status_map/views.py

Olavur Mortensen s103261, Wojciech Pawlak s091820

'''

from django.shortcuts import render

from twitter_region_sentiment.data_collector import DataCollector, RegionError
from twitter_region_sentiment.simple_sentiment_analyzer import SimpleSentimentAnalyzer

def index(request):
    '''
    Renders the view "index.html" - main webpage of web application.
    Collects data to show in view. DataCollector is called to get the data
    to show and analyze. SimpleSentimentAnalyzer is called to analyze the collected
    tweets. The statistics are collected and passed to view.
    '''
    
    errors = []
    tweets_to_show = [] # tweet' fields that are rendered on the page
    texts_to_analyse = [] # texts of tweets that are analysed for sentiment
    
    
    dc = DataCollector()
    
    region = 'Anker Engelunds Vej 1, Denmark' # default region
    radius = 15 # default radius
    user_search = 0 

    if 'q' not in request.GET: # first start of website
        context = {'first_map': region,
            'errors':errors,
            'user_search':user_search}
        return render(request, 'twitter_region_sentiment/index.html', context)
    elif 'q' in request.GET and request.GET['q'] != '': # normal behaviour
        region = request.GET['q']
        user_search = 1 
    elif 'q' in request.GET and request.GET['q'] == '': # empty textfield
        errors.append('No region specified. Default region used.')
        region = 'Anker Engelunds Vej 1, Denmark' 
        context = {'first_map': region,
            'errors': errors,
            'user_search': user_search}
        return render(request, 'twitter_region_sentiment/index.html', context)


    if 'r' in request.GET and request.GET['r'] != '':
        radius = request.GET['r']
        
    try:
        tweets = dc.retrieve_tweets(region, radius)       
    except RegionError as r_error:
        # exception is thrown when
        errors.append(r_error.value)
        region = 'Anker Engelunds Vej 1, Denmark' 
        context = {'first_map': region,
            'errors': errors,
            'user_search': user_search}
        return render(request, 'twitter_region_sentiment/index.html', context)
                   
    # extract fields from tweets to show and texts to analyze as lists
    for tweet in tweets:
        tweets_to_show.append({
                        'text': tweet.text,
                        'user': tweet.user.AsDict()['screen_name'],
                        'datetime': tweet.AsDict()['created_at'],
                        'image': tweet.user.AsDict()['profile_image_url']
                        })
        texts_to_analyse.append(tweet.text)         
            
            
    ssa = SimpleSentimentAnalyzer()
    
    moods = ssa.get_region_moods(texts_to_analyse)
    
    for idx, tweet in enumerate(tweets_to_show):
        tweet['mood'] = moods[idx]
        
        if moods[idx] == 0:
            tweet['moodColor'] = 'blue'
        elif moods[idx] < 0:
            tweet['moodColor'] = 'red'
        elif moods > 0:
            tweet['moodColor'] = 'green'
        else:
            tweet['moodColor'] = 'black'
    
    mood_stats = ssa.prepare_mood_stats(moods)

    # 20 most frequent words are displayed
    topics_temp = ssa.get_top_word_frequencies(texts_to_analyse)[0:21]
    
    topics = []
    for topic in topics_temp:
        topics.append({'word':topic[0], 'freq':topic[1], 'mood':topic[2]})
    
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
    
    return render(request, 'twitter_region_sentiment/index.html', context)
