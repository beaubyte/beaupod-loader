import os
from dotenv import load_dotenv
import requests # imports requests for lastfm api
from ytmusicapi import YTMusic # imports unofficial ytmusic api
from yt_dlp import ytdlp # imports yt-dlp
from mutagen.mp4 import MP4, MP4Cover

def main():
    print ('starting beaupod-loader')

    # lastfm api configuration --------------
    api_endpoint = 'http://ws.audioscrobbler.com/2.0/'
    load_dotenv()
    API_KEY = os.getenv('API_KEY') # not required for searching top songs, can be blank and still return data
    USERNAME = os.getenv('LASTFM_USERNAME')

    # yt music api configuration --------------
    yt = YTMusic() # this can be authenticated for more features, for now it does not need auth
    
    # parameters to send to lastfm api
    parameters = {
        'method' : 'user.gettoptracks',
        'user' : USERNAME,
        'api_key' : API_KEY,
        'format' : 'json',
        'limit' : 50,
        'period' : '6months'
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

    # query youtube music for songs and append first result to list
    url_list = []
    for idx in song_list:
        results = yt.search(song_list[idx] + " " + artist_list[idx], filter='songs')
        if results:
            song = results[0]
            song_id = song['videoId']
            url = "https://music.youtube.com/watch?v=" + song_id
            url_list.append(url)
        else:
            url_list.append("about:blank")

    # use yt-dlp to download song file and attach metadata
    for url in url_list:
        ytdlp.download(url)
        


    




if __name__ == "__main__":
    main()