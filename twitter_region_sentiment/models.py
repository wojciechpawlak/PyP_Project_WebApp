'''
02820 Python Programming E12, DTU

models.py

Olavur Mortensen s103261, Wojciech Pawlak s091820
'''

from django.db import models

class Map(models.Model):
    address = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.address

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.tweet_id
    
class RegionQuery(models.Model):
    region = models.CharField(max_length=200)
    radius = models.IntegerField()
    query_date = models.DateTimeField('date mined')
    
    def __unicode__(self):
        return self.region