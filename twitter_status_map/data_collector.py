'''
Created on 11-12-2012

@author: Wojtek
'''

import twitter
from googlemaps import GoogleMaps, GoogleMapsError

class DataCollector(object):
    '''
    Class fo fetching data from Twitter
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.coordinates = (0,0)
        self.api = twitter.Api()
        self.texts = []