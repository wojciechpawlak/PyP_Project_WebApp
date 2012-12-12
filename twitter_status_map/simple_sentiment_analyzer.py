'''
02820 Python Programming E12, DTU

simple_sentiment_analyzer.py

Olavur Mortensen s103261, Wojciech Pawlak s091820
'''
import operator
import numpy as np

from twitter_status_map.util import clean_tweet_text

class SimpleSentimentAnalyzer(object):
    '''
    classdocs
    '''


    def __init__(self, wordlist_name='afinn'):
        '''
        Constructor
        '''
        # afinn is a dictionary with words as keys and their positivity/negativity as values.
        if wordlist_name == 'afinn':
            self.wordlist = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("resources/AFINN-111.txt") ]))
        else:
            self.wordlist = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("resources/EmotionLookupTable.txt") ]))
            self.wordlist.update(dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("resources/EmoticonLookupTable.txt") ])))  
        
        
    def get_tweet_text_mood(self, text):
        '''
        text is a string.
        
        getMood gets the positivity/negativity (mood) of a string (tweet).
        
        Returns an integer, or the string 'None' if no mood is associated with it.
        '''
        
        clean_text = clean_tweet_text(text)
        
        # The mood is the sum of the moods of each word.
        text_mood = sum(map(lambda word: self.wordlist.get(word, 0), clean_text))
        
        # Check whether any mood was found.
        check = 0
        for i in clean_text:
            if self.wordlist.get(i,100) != 100: # ?
                check=1
        
        if check == 0:
            text_mood='None'
        
        return text_mood

    def get_region_moods(self, texts):
        '''
        tweetList is a list of strings.
        
        Gets the mood of each string in the list, and returns a list of moods (integers), and potentially the string 'None' (see 'get_mood').
        '''
        
        moods = [ self.get_tweet_text_mood(text) for text in texts ]
        
        return moods
    
    
    def clean_none_moods(self, moods):
        '''
        moodList is a list of integers, and possibly the string 'None'
        
        cleanNoneMoods removes the string 'None' if found.
        
        Returns a list of integers.
        '''
        
        moodOut=[]
        
        for i in moods:
            if i != 'None':
                moodOut.append(i)
        
        return moodOut

        
    def prepare_mood_stats(self, moodList):
        
        moodListClean = self.clean_none_moods(moodList)
        moodListClean = np.array(moodListClean)
        sd = np.std(moodListClean)
        mean = np.mean(moodListClean)
        positives = sum(moodListClean>0)
        negatives = sum(moodListClean<0)
        neutrals = sum(moodListClean==0)
        NoMood = len(moodList)-len(moodListClean)
        
        return {'sd':sd,'mean':mean,'positives':positives,'negatives':negatives,'neutrals':neutrals,'NoMood':NoMood}
    
    def get_top_word_frequencies(self, texts):
        '''
        texts is a list of strings.
        
        getTopic finds the frequencies of words in texts.
        
        Returns a list of tuples in the format: (word,frequency,mood)
        See 'getMood' for explaination of mood.
        '''
        
        # Making the list of sentences into a list of words
        temp=[]
        for i,j in enumerate(texts):
            temp.append(clean_tweet_text(j))
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
            wfm.append((j[0],j[1],self.wordlist.get(j[0],'None')))
        wfm2=[]
        for i,j in enumerate(wfm):
            if j[2]!='None':
                wfm2.append(j)
        
        return wfm2
        