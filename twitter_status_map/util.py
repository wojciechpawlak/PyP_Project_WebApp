import re

def clean_tweet_text(tweet_text):
    '''
    tweet is a string.
    
    cleanTweet removes words that are not letters A-Z or a-z, and returns a list of remaining words.
    '''
    
    tweet_text=tweet_text.lower().split()
    
    clean_tweet_text = []
    for word in tweet_text:
        if re.match("^[A-Za-z]*$", word):
            clean_tweet_text.append(word)
    
    return clean_tweet_text





        



























