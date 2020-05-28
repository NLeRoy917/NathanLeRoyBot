import tweepy

class API():
    '''
    My custom API to make tweepy evern higher level
    '''
    def __init__(self,api):
        self._api = api
    
    def post_tweet(self,status):
        status = self._api.update_status(status)
        return status