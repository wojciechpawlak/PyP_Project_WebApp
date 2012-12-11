import re

afinn = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("twitter_status_map/AFINN/AFINN-111.txt") ]))

def removeReTweets(tweetList):
    tw=[]
    for t in tweetList:
        if t.text[0:4]!='RT @':
            tw.append(t)
    return tw

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
    
    check=0
    for i,j in enumerate(tweet):
        if afinn.get(j,100)!=100:
            check=1
    if check==0:
        mood='None'
    
    return mood

def getRegionMood(tweetList):
    
    moodList=[ getMood(tweet) for tweet in tweetList]
    
    return moodList

def cleanNoneMoods(moodList):
    moodOut=[]
    
    for i,j in enumerate(moodList):
        if j!='None':
            moodOut.append(j)
    
    return moodOut


  
'''
from twitter_status_map.util import *

text='RT @MarilynMonroeID: People may doubt what you say, but they will always believe what you do.'

cleanTweet(text)


'''
