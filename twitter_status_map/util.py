import re

afinn = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("twitter_status_map/AFINN/AFINN-111.txt") ]))

def cleanTweet(tweet):
    
    tweet=tweet.lower().split()
    
    tw=[]
    # tweet = [unicode(elem) for elem in tweet]
    for word in tweet:
        if re.match("^[A-Za-z]*$", word):
            tw.append(word)
    
    return tw

def getMood(text):
    tweet=cleanTweet(text)
    
    mood=sum(map(lambda word: afinn.get(word, 0), tweet))
    
    return mood

def getAreaMood(tweetList):
    
    moodList=[ getMood(tweet) for tweet in tweetList]
    
    return moodList



  
'''
from twitter_status_map.util import *

text='RT @MarilynMonroeID: People may doubt what you say, but they will always believe what you do.'

cleanTweet(text)


'''