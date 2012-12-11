import re
import operator

# afinn is a dictionary with words as keys and their positivity/negativity as values.
afinn = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("twitter_status_map/AFINN/AFINN-111.txt") ]))

def remove_retweets(tweetList):
    '''
    Removes retweets.
    
    tweetList is a list of tweet objects returned from the twitter api.
    
    if a tweet starts with 'RT @' it is removed.
    '''
    
    tw=[]
    for t in tweetList:
        if t.text[0:4]!='RT @':
            tw.append(t)
    
    return tw

def cleanTweet(tweet):
    '''
    tweet is a string.
    
    cleanTweet removes words that are not letters A-Z or a-z, and returns a list of remaining words.
    '''
    
    tweet=tweet.lower().split()
    
    tw=[]
    for word in tweet:
        if re.match("^[A-Za-z]*$", word):
            tw.append(word)
    
    return tw

def getMood(text):
    '''
    text is a string.
    
    getMood gets the positivity/negativity (mood) of a string (tweet).
    
    Returns an integer, or the string 'None' if no mood is asociated with it.
    '''
    
    tweet=cleanTweet(text)
    
    # The mood is the sum of the moods of each word.
    mood=sum(map(lambda word: afinn.get(word, 0), tweet))
    
    # Check whether any mood was found.
    check=0
    for i,j in enumerate(tweet):
        if afinn.get(j,100)!=100:
            check=1
    if check==0:
        mood='None'
    
    return mood

def getRegionMood(tweetList):
    '''
    tweetList is a list of strings.
    
    Gets the mood of each string in the list, and returns a list of moods (integers), and potentially the string 'None' (see 'getMood').
    '''
    
    moodList=[ getMood(tweet) for tweet in tweetList]
    
    return moodList

def cleanNoneMoods(moodList):
    '''
    moodList is a list of integers, and possibly the string 'None'
    
    cleanNoneMoods removes the string 'None' if found.
    
    Returns a list of integers.
    '''
    
    moodOut=[]
    
    for i,j in enumerate(moodList):
        if j!='None':
            moodOut.append(j)
    
    return moodOut

def getTopic(texts):
    '''
    texts is a list of strings.
    
    getTopic finds the frequencies of words in texts.
    
    Returns a list of tuples in the format: (word,frequency,mood)
    See 'getMood' for explaination of mood.
    '''
    
    # Making the list of sentences into a list of words
    temp=[]
    for i,j in enumerate(texts):
        temp.append(cleanTweet(j))
    words=[]
    for i,j in enumerate(temp):
        for n,m in enumerate(j):
            words.append(m)
    
    # Getting the frequencies of words in a dictionary
    freq={}
    for i,j in enumerate(words):
        if j in freq:
            freq[j]+=1
        else:
            freq[j]=1
    
    # Getting the words sorted from highest to lowest frequency
    fvalues=freq.values().sort(reverse=True)
    words_sorted = sorted(freq.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    # Getting the final (word,frequency,mood) list
    wfm=[]
    for i,j in enumerate(words_sorted):
        wfm.append((j[0],j[1],afinn.get(j[0],'None')))
    wfm2=[]
    for i,j in enumerate(wfm):
        if j[2]!='None':
            wfm2.append(j)
    
    return wfm2
        



























