from lib.Model import Model
from lib.Utils import Utils
from lib.API import API

# initialize objects
utils = Utils()
model_nathan = Model()
model_hailey = Model()

import logging
import time
import tweepy
import re
import random
from configparser import ConfigParser

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, filename="bot.log",
                        datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info('Starting Up Bot.')

CONFIG_FILE = 'config.ini'

# initialialize config file
config = ConfigParser()
config.read(CONFIG_FILE)

logging.info('Reading in API keys')

# extract secrets
API_KEY_NATHAN = config.get('TWITTER','api_key_nathan')
API_KEY_SECRET_NATHAN = config.get('TWITTER','api_key_secret_nathan')
ACCESS_TOKEN_NATHAN = config.get('TWITTER','access_token_nathan')
ACCESS_TOKEN_SECRET_NATHAN = config.get('TWITTER','access_token_secret_nathan')

API_KEY_HAILEY = config.get('TWITTER','api_key_hailey')
API_KEY_SECRET_HAILEY = config.get('TWITTER','api_key_secret_hailey')
ACCESS_TOKEN_HAILEY = config.get('TWITTER','access_token_hailey')
ACCESS_TOKEN_SECRET_HAILEY = config.get('TWITTER','access_token_secret_hailey')

# extract username
USER = config.get('TWITTER','user')
logging.info('Running bot for: {}.'.format(USER))

logging.info('Extracting bot parameters.')
# extract bot running parameters
SLEEP_TIME = int(config.get('BOT','sleep_time')) # mins
TEMP = float(config.get('BOT','temperature'))
MAX_LENGTH = int(config.get('BOT','max_length'))
MIN_LENGTH = int(config.get('BOT','min_length'))

logging.info('Authenticating twitter.')

# authenticate
auth_nathan = tweepy.OAuthHandler(API_KEY_NATHAN, API_KEY_SECRET_NATHAN)
auth_nathan.set_access_token(ACCESS_TOKEN_NATHAN, ACCESS_TOKEN_SECRET_NATHAN)

# authenticate
auth_hailey = tweepy.OAuthHandler(API_KEY_HAILEY, API_KEY_SECRET_HAILEY)
auth_hailey.set_access_token(ACCESS_TOKEN_HAILEY, ACCESS_TOKEN_SECRET_HAILEY)

# create api object
# and pass it to my higher level API to act as a bot
api_nathan = tweepy.API(auth_nathan)
bot_nathan = API(api_nathan)

# create api object
# and pass it to my higher level API to act as a bot
api_hailey = tweepy.API(auth_hailey)
bot_hailey = API(api_hailey)

# load and init model
model_nathan.load_model(run_name='run1')
model_hailey.load_model(run_name='run2')

try:
    while True:
        
        length = random.randint(MIN_LENGTH,MAX_LENGTH) # length of tweet
        
        tweet_nathan = model_nathan.generate(length=length, temperature=TEMP)
        forbidden_nathan = utils.check_forbidden_words(tweet_nathan)

        tweet_hailey = model_nathan.generate(length=length, temperature=TEMP)
        forbidden_hailey = utils.check_forbidden_words(tweet_hailey)

        while forbidden_nathan:
            logging.warn('Forbidden tweet found! \n{}\n'.format(tweet_nathan))
            logging.warn('Regenerating tweet.')
            tweet_nathan = model_nathan.generate(length=length, temperature=TEMP)
            forbidden_nathan = utils.check_forbidden_words(tweet_nathan)

        while forbidden_hailey:
            logging.warn('Forbidden tweet found! \n{}\n'.format(tweet_hailey))
            logging.warn('Regenerating tweet.')
            tweet_nathan = model_hailey.generate(length=length, temperature=TEMP)
            forbidden_hailey = utils.check_forbidden_words(tweet_hailey)
        
        logging.info('Checks passed. Posting tweets: \n{}\n \n{}\n'.format(tweet_nathan,tweet_hailey))

        #print(tweet)
        bot_nathan.post_tweet(tweet_nathan)
        bot_hailey.post_tweet(tweet_hailey)

        logging.info('Tweet posted. Sleeping for {} min'.format(SLEEP_TIME))

        time.sleep(SLEEP_TIME*60) # sleep - seconds to mins

except KeyboardInterrupt:
    logging.info('Exiting bot. Goodbye.')

# for i in range(10):
#     tweet = model.generate()
#     print('{}.'.format(i),tweet)
