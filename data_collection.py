# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:18:59 2021

@author: phadk
"""

import pandas as pd
import sys
sys.path.insert(0, r'C:\Users\phadk\Desktop\Work\projects\scrapers\spotify')
from SpotifyAPI import SpotifyAPI


client_id = '4afc2ca68fc84441a32bc7fdbef9b296'
client_secret = '3336c0c6cd754ca29367557e2aa5cd9c'

spotify = SpotifyAPI(client_id,client_secret)

df = pd.read_csv(r"C:\Users\phadk\Desktop\Work\projects\portfolio\Spotify_eda\playlist.csv")
playlist_ids = list(df['playlist_id'])
year = 2020
track_info = []

for p in playlist_ids:
    playlist_details = spotify.get_playlist_tracks(p)
    total_tracks = len(playlist_details['items'])
    
    for t in range(0,total_tracks):
        base = playlist_details['items'][t]['track']
        row = [year,base['id'],base['name'],base['artists'][0]['name'],base['album']['release_date'],base['popularity']]
        track_info.append(row)
    
    year = year-1

df_out = pd.DataFrame(track_info, columns = ['billboard_year','song_id','name','artist','release_date','popularity'])

song_ids = list(df_out['song_id'])
features = []
feature_name = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 
           'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']

for s in song_ids:
    data = spotify.get_features(s)
    values = data.values()
    features.append(values)

df_feature = pd.DataFrame(features, columns = feature_name)

data = pd.merge(df_out, df_feature, left_on='song_id', right_on='id', how='left').drop('id', axis=1)
data.to_csv(r"C:\Users\phadk\Desktop\Work\projects\portfolio\Spotify_eda\data.csv")
