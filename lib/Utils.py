import re
import tweepy

class Utils():

    def __init__(self):
        '''
        Initialize Utilities object
        '''
        self.forbidden_words = [
            ' fuck ',
            ' shit ',
            'sydney',
            ' trump ',
            ' pussies ',
        ]
        return
    
    def clean_tweet(self,text):
        '''
        Method to clean the text of a tweet. Uses regex to remove URLs, remove mentions,
        remove unncessary whitespace, and remove redundant spaces.
            :text(string) - text to clean

            return text(string) - a cleaned version of the text
        '''
        text = re.sub(r'http\S+', '', text)   # Remove URLs
        text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  # Remove @ mentions
        text = text.strip(" ")   # Remove whitespace resulting from above
        text = re.sub(r' +', ' ', text)   # Remove redundant spaces

        # Handle common HTML entities
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&amp;', '&', text)
        
        return text
    
    def download_tweets(self,api,user,outfile='tweets.txt'):
        
        texts = []
        context_labels = []

        print("Downloading {}'s Tweets...".format(user))
        all_tweets = tweepy.Cursor(api.user_timeline,
                               screen_name=user,
                               count=200,
                               tweet_mode='extended',
                               include_rts=False).pages(16)
        for page in all_tweets:
            for tweet in page:
                tweet_text = self.clean_tweet(tweet.full_text)
                if tweet_text is not '':
                    texts.append(tweet_text)
                    context_labels.append(user)
        
        if outfile:
            with open(outfile,'w') as f:
                for tweet in texts:
                    f.write(tweet + '\n')

        return texts,context_labels
    
    def get_tweets_from_file(self,file):
        '''
        Open file, read in tweets and return list
            :file(string) - path to file containing tweets

            returns tweet_list(list) - list of tweets
        '''

        with open(file,'r') as f:
            tweet_list = f.readlines()
        
        return tweet_list
    
    def check_forbidden_words(self,tweet):
        '''
        Loop through the forbidden words list and ensure our tweet
        doesn't contain any of them
        '''
        tweet = tweet.lower()
        for word in self.forbidden_words:
            if word.lower() in tweet:
                return True # found, return True
            
        return False # never found anything return False
