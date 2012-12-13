"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test.client import Client
#from django.test import TestCase
from django.utils import unittest

from twitter_region_sentiment.data_collector import DataCollector, RegionError
from twitter_region_sentiment.simple_sentiment_analyzer import SimpleSentimentAnalyzer

from twitter_region_sentiment.models import Tweet

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

        
#class QueryModelTest(unittest.TestCase):
#    def setUp(self):
#        self.c = Client()