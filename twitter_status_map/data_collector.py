"""
02820 Python Programming E12, DTU

data_collector.py

Olavur Mortensen s103261, Wojciech Pawlak s091820
"""
import twitter
from googlemaps import GoogleMaps, GoogleMapsError

import time

from twitter_status_map.util import remove_retweets

DEFAULT_REGION = 'Anker Engelunds Vej 1, Denmark'
DEFAULT_RADIUS = 25

LANG = 'en'
DIST_UNIT = 'km'
MAX_TWEETS_PER_PAGE = 100
NUM_PAGES = 3

class RegionError(Exception):
    '''
    Exception raised when GoogleMapsError is raised and passed to outer scope
    when Google Maps API cannot find coordinates for specified region
    '''
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DataCollector(object):
    '''
    Class for fetching collecting data from specified region from Twitter Search API
    
    Number of pages with tweets retrieved for project: 3
    
    A Python Twitter Search API wrapper: http://code.google.com/p/python-twitter/
    is used for individual calls to Twitter Search API.
    For more information about Twitter Search API parameters and limitations:
    https://dev.twitter.com/docs/api/1/get/search
    and
    https://dev.twitter.com/docs/using-search
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.region = DEFAULT_REGION
        self.radius = DEFAULT_RADIUS

            
        self.lang = LANG
        self.dist_unit = DIST_UNIT
        self.per_page = MAX_TWEETS_PER_PAGE
        self.num_pages = NUM_PAGES
        
        self.api = twitter.Api()
        self.gmaps = GoogleMaps()
        
    def __retrieve_tweets_by_geocode(self):
        '''
        Output: list of tweets retrieved for query with geo location
        
        Calls a Twitter Search API a fixed number of times (num_pages times) with:
        term = NONE,
        geocode equal to tuple of:
            latitude and longitude that a Google Maps API specify for,
            radius specified in kilometeres
        lang='en',
        per_page=100, so maximum possible
        '''
                
        tweets = []
        
        try:
            lat, lng = self.gmaps.address_to_latlng(self.region.encode('utf8','ignore'))
        except GoogleMapsError:
            return []
        
        for num_page in range(1,self.num_pages):
            tweets = tweets + self.api.GetSearch(geocode=(str(lat),str(lng),str(self.radius)+self.dist_unit),lang=LANG,per_page=self.per_page,page=num_page)

        return tweets
            
            
    def __retrieve_tweets_by_region(self):
        '''
        Output: list of tweets retrieved for query with region as term
        
        Calls a Twitter Search API a fixed number of times (num_pages times) with:
        term = region,
        geocode = None
        lang='en',
        per_page=100, so maximum possible
        
        http://code.google.com/p/python-twitter/
        For more information about Twitter Search API:
        '''
        
        tweets = []
        
        for num_page in range(1,self.num_pages):
            tweets = tweets + self.api.GetSearch(term=self.region,lang=self.lang,per_page=self.per_page, page=num_page)
        
        return tweets

            
    def retrieve_tweets(self, region, radius):
        '''
        Input: string with region name and number of radius from the center of this region
        Output:
        
        Retrieves tweets from Twitter Search API using different calls
        
        '''
        # check the input parameters  
        if region == '':
            self.region = DEFAULT_REGION
        else:
            self.region = region
           
        if region <= 0:
            self.radius = DEFAULT_RADIUS
        else:
            self.radius = radius
        
        
        # retrieve tweets using two different Twitter Search API queries one after another
        try:
            all_tweets = self.__retrieve_tweets_by_geocode()
        except GoogleMapsError:
            raise RegionError("Invalid region")
        all_tweets = all_tweets + self.__retrieve_tweets_by_region()
    
        # uniquify list of tweets through making a set and convert it back to list (faster methods exist)
        all_tweets_set = set(all_tweets)
        all_tweets = list(all_tweets_set)
        
        # sort tweets by date
        all_tweets = sorted(all_tweets, key=lambda t: time.strptime(t.created_at, "%a, %d %b %Y %H:%M:%S +0000"), reverse=True)
            
        #            
        all_tweets = remove_retweets(all_tweets)
        
        return all_tweets
        