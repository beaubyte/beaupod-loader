import requests
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL

# need to still do api key stuff
API_KEY = ''
USERNAME = ''

def main():
    api_endpoint = 'http://ws.audioscrobbler.com/2.0/'

    # parameters to send to api
    parameters = {
        'method' : 'user.gettoptracks',
        'user' : USERNAME,
        'api_key' : API_KEY,
        'format' : 'json',
        'limit' : 5,
        'period' : '3month'
    }

    # get data from api
    response = response.get(api_endpoint, parameters)
    response_data = response.json

    # get artists and songs and build array
    if 'toptracks' in response_data:
        
        


