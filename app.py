import os
from dotenv import load_dotenv
import requests # imports requests for lastfm api
from ytmusicapi import YTMusic # imports unofficial ytmusic api
from yt_dlp import YoutubeDL
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
        'limit' : 5,
        'period' : 'overall'
    }

    # get data from api
    response = requests.get(api_endpoint, parameters)

    if (response.status_code == 200):
        response_data = response.json()
        print ('api request succeeded')
    else:
        print ('lastfm api call failed with http status code: ' + str(response.status_code))
        exit(1)
        
    # get lastfm song objects and build array
    song_list = []
    if ('toptracks' in response_data):
        for idx, track in enumerate(response_data['toptracks']['track'], 1):
            song_list.append(track)
            print("Added track: " + track['artist']['name'],end=' - ')
            print(track['name'])
    else:
        print('lastfm response data is malformed')

    # query youtube music for songs and append first result to list
    result_list = []
    for i in range(len(song_list)):
        results = yt.search(song_list[i]['name'] + " " + song_list[i]['artist']['name'], filter='songs')
        if results:
            song = results[0]
            result_list.append(song)
            print('Found song: ' + song['title'] + ' - ' + song['artists'][0]['name'])
        else:
            result_list.append("error")

    # use yt-dlp to download song file and attach metadata
    for idx, result in enumerate(result_list):
        # options passed to youtube-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
            }],
            'postprocessor_args': [
                '-ar', '44100', # resamples audio to the highest supported rate by 5th gen ipod
                '-c:a', 'libfdk-aac' 
            ],
            'outtmpl': str(song_list[idx]['name'] + " - " + song_list[idx]['artist']['name'])
        }
        with YoutubeDL(ydl_opts) as ytdlp:
            song_id = result['videoId']
            url = "https://music.youtube.com/watch?v=" + song_id
            ytdlp.download(url)

        # starts building metadata for the m4a file
        audio_file = MP4(str(song_list[idx]['name'] + " - " + song_list[idx]['artist']['name'] + ".m4a"))
        audio_file["\xa9nam"] = result["title"]
        print('Attached title: ' + result["title"])
        audio_file["\xa9ART"] = result["artists"][0]["name"]
        print('Attached artist: ' + result["artists"][0]["name"])
        audio_file["\xa9alb"] = result["album"]["name"]
        print('Attached album: ' + result["album"]["name"])
        album_art = requests.get(song_list[idx]['image'][-1]['#text'])
        if album_art.status_code == 200:
            audio_file["covr"] = [MP4Cover(album_art.content, imageformat=MP4Cover.FORMAT_JPEG)]
        audio_file.save()





if __name__ == "__main__":
    main()