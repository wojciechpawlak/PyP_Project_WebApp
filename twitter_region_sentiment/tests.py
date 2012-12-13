'''
02820 Python Programming E12, DTU

tests.py

Olavur Mortensen s103261, Wojciech Pawlak s091820
'''

from django.test.client import Client
#from django.test import TestCase
from django.utils import unittest

from twitter_region_sentiment.data_collector import DataCollector, RegionError
from twitter_region_sentiment.simple_sentiment_analyzer import SimpleSentimentAnalyzer

from twitter_region_sentiment.models import Tweet, RegionQuery

class DataCollectorTest(unittest.TestCase):
    
    def setUp(self):
        self.dc = DataCollector()
    
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)
        

class SimpleSentimentAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.dc = SimpleSentimentAnalyzer()
        self.pos_tweet = 'Congrats SolarCitys discount approach to going public pays off'
        self.neg_tweet = 'Done with wack ass finals!!!'
        
    def test_get_tweet_text_mood(self):
        result_pos = self.dc.get_tweet_text_mood(self.pos_tweet)
        self.assertEqual(2,result_pos)
        
        result_neg = self.dc.get_tweet_text_mood(self.neg_tweet)
        self.assertEqual(-4,result_neg)

class IndexControllerTest(unittest.TestCase):
    def setUp(self):
        self.c = Client()
#    
#    def test_start_page(self):
#    response = c.post('/twitter/', {'username': 'john', 'password': 'smith'})
#    self.assertEqual(response.status_code, 200)
#>>> response = c.get('/customer/details/')
#>>> response.content


#    def my_func(a_list, idx):
#        """
#        >>> a = ['larry', 'curly', 'moe']
#        >>> my_func(a, 0)
#        'larry'
#        >>> my_func(a, 1)
#        'curly'
#        """
#        return a_list[idx]

#class TweetModelTest(unittest.TestCase):
#    def setUp(self):
#        self.tweet = Tweet.objects.create(tweet_id="")

        
#class RegionQueryModelTest(unittest.TestCase):
#    def setUp(self):
#        self.c = Client()