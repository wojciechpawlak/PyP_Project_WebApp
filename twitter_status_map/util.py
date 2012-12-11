import re
import operator

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

def getTopic(texts):
    temp=[]
    for i,j in enumerate(texts):
        temp.append(cleanTweet(j))
    
    words=[]
    for i,j in enumerate(temp):
        for n,m in enumerate(j):
            words.append(m)
    
    freq={}
    for i,j in enumerate(words):
        if j in freq:
            freq[j]+=1
        else:
            freq[j]=1
    
    fvalues=freq.values().sort(reverse=True)
    
    words_sorted = sorted(freq.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    wfm=[]
    for i,j in enumerate(words_sorted):
        wfm.append((j[0],j[1],afinn.get(j[0],'None')))
    
    wfm2=[]
    for i,j in enumerate(wfm):
        if j[2]!='None':
            wfm2.append(j)
    
    return wfm2
        



























