'''
02820 Python Programming E12, DTU

PyP_Project_WebApp/twitter_status_map/util.py

Olavur Mortensen s103261, Wojciech Pawlak s091820
'''

import re

def clean_tweet_text(tweet_text):
    '''
    tweet is a string.
    
    cleanTweet removes words that are not letters A-Z or a-z, and returns a list of remaining words.
    '''
    
    tweet_text = tweet_text.lower().split()
    
    cleaned_text = []
    for word in tweet_text:
        if re.match("^[A-Za-z]*$", word):
            cleaned_text.append(word)
    
    return cleaned_text





        



























