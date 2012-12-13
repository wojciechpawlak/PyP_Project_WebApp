'''
02820 Python Programming E12, DTU

simple_sentiment_analyzer.py

Olavur Mortensen s103261, Wojciech Pawlak s091820
'''
import operator
import numpy as np

from twitter_region_sentiment.util import clean_tweet_text

class SimpleSentimentAnalyzer(object):
    '''
    classdocs
    '''


    def __init__(self, wordlist_name='afinn'):
        '''
        Constructor
        '''
        # wordlist is a dictionary with words as keys and mood as values.
        if wordlist_name == 'afinn':
            self.wordlist = dict(map(lambda (k, v): (k, int(v)), [ line.split('\t') for line in open("resources/AFINN-111.txt") ]))
        else:
            self.wordlist = dict(map(lambda (k, v): (k, int(v)), [ line.split('\t') for line in open("resources/EmotionLookupTable.txt") ]))
            self.wordlist.update(dict(map(lambda (k, v): (k, int(v)), [ line.split('\t') for line in open("resources/EmoticonLookupTable.txt") ])))  
        
        
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
            if self.wordlist.get(i, 100) != 100: # ?
                check = 1
        
        if check == 0:
            text_mood = 'None'
        
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
        
        mood_out = []
        
        for i in moods:
            if i != 'None':
                mood_out.append(i)
        
        return mood_out

        
    def prepare_mood_stats(self, mood_list):
        '''
        Output: dictionary of statistics on the input
        
        Input: list of integers (moods)
        '''
        mood_list_clean = self.clean_none_moods(mood_list)
        mood_list_clean = np.array(mood_list_clean)
        std = np.std(mood_list_clean)
        mean = np.mean(mood_list_clean)
        positives = sum(mood_list_clean>0)
        negatives = sum(mood_list_clean<0)
        neutrals = sum(mood_list_clean==0)
        no_mood = len(mood_list)-len(mood_list_clean)
        
        return {'sd':std, 'mean':mean,
            'positives':positives,
            'negatives':negatives,
            'neutrals':neutrals,
            'NoMood':no_mood}
    
    def get_top_word_frequencies(self, texts):
        '''
        texts is a list of strings.
        
        getTopic finds the frequencies of words in texts.
        
        Returns a list of tuples in the format: (word,frequency,mood)
        See 'getMood' for explaination of mood.
        '''
        
        # Making the list of sentences into a list of words
        temp = []
        for texts_elem in texts:
            temp.append(clean_tweet_text(texts_elem))
        words = []
        for temp_elem in temp:
            for temp_elem2 in temp_elem:
                words.append(temp_elem2)
        
        # Getting the frequencies of words in a dictionary
        freq = {}
        for words_elem in words:
            if words_elem in freq:
                freq[words_elem] += 1
            else:
                freq[words_elem] = 1
        
        # Getting the words sorted from highest to lowest frequency
        words_sorted = sorted(freq.iteritems(),
            key=operator.itemgetter(1),
            reverse=True)
        
        # Getting the final (word,frequency,mood) list
        wfm = []
        for words_sorted_elem in words_sorted:
            wfm.append((words_sorted_elem[0],
                words_sorted_elem[1],
                self.wordlist.get(words_sorted_elem[0], 'None')))
        wfm2 = []
        for wfm_elem in wfm:
            if wfm_elem[2] != 'None':
                wfm2.append(wfm_elem)
        
        return wfm2
        
