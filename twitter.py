import requests
from requests.auth import HTTPBasicAuth
from secrets import consumer_key, consumer_secret

class Twitter():
    def __init__(self):
        self.renew_token()

    def renew_token(self):
        response = requests.post(
            'https://api.twitter.com/oauth2/token',
            data={'grant_type': 'client_credentials'},
            auth=HTTPBasicAuth(consumer_key, consumer_secret))
        if response.status_code == 200:
            self.token = response.json()['access_token']

    def search(self, query):
        response = requests.get(
            'https://api.twitter.com/1.1/search/tweets.json',
            headers={'Authorization': 'Bearer %s' % self.token},
            params={'q': query})
        if response.status_code == 200:
            tweets = response.json()['statuses']
            return [(t['created_at'], t['text']) for t in tweets]
