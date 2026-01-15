import os
from dotenv import load_dotenv
import requests # imports requests for lastfm api
from ytmusicapi import YTMusic # imports unofficial ytmusic api
from yt_dlp import YoutubeDL # imports yt-dlp

def main():
    print ('starting beaupod-loader')
    api_endpoint = 'http://ws.audioscrobbler.com/2.0/'
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    USERNAME = os.getenv('USERNAME')
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
    response = requests.get(api_endpoint, parameters)

    if (response.status_code == 200):
        response_data = response.json()
        print ('api request succeeded')
    else:
        print ('lastfm api call failed with http status code: ' + str(response.status_code))
        exit(1)
        
    # get artists and songs and build array
    artist_list = []
    song_list = []
    if ('toptracks' in response_data):
        for idx, track in enumerate(response_data['toptracks']['track'], 1):
            artist_list.append(track['artist']['name'])
            print("Added track: " + track['artist']['name'],end=' - ')
            song_list.append(track['name'])
            print(track['name'])
    else:
        print('lastfm response data is malformed')

if __name__ == "__main__":
    main()