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
API_KEY = config.get('TWITTER','api_key')
API_KEY_SECRET = config.get('TWITTER','api_key_secret')
ACCESS_TOKEN = config.get('TWITTER','access_token')
ACCESS_TOKEN_SECRET = config.get('TWITTER','access_token_secret')

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
auth_nathan = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth_nathan.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# create api object
# and pass it to my higher level API to act as a bot
api_nathan = tweepy.API(auth_nathan)
bot_nathan = API(api_nathan)

# load and init model
model_nathan.load_model(run_name='run1')
model_hailey.load_model(run_name='run2')

try:
    while True:
        
        length = random.randint(MIN_LENGTH,MAX_LENGTH) # length of tweet
        
        tweet = model_nathan.generate(length=length, temperature=TEMP)
        forbidden = utils.check_forbidden_words(tweet)

        while forbidden:
            logging.warn('Forbidden tweet found! \n{}\n'.format(tweet))
            logging.warn('Regenerating tweet.')
            tweet = model_nathan.generate(length=length, temperature=TEMP)
            forbidden = utils.check_forbidden_words(tweet)
        
        logging.info('Checks passed. Posting tweet: \n{}\n'.format(tweet))

        #print(tweet)
        bot_nathan.post_tweet(tweet)

        logging.info('Tweet posted. Sleeping for {} min'.format(SLEEP_TIME))

        time.sleep(SLEEP_TIME*60) # sleep - seconds to mins

except KeyboardInterrupt:
    logging.info('Exiting bot. Goodbye.')

# for i in range(10):
#     tweet = model.generate()
#     print('{}.'.format(i),tweet)
