# Analyzing Billboards year-end top 100 Songs

## Problem Statement

> Every year Billboard realeases a list of 100 songs that dominated the music industry with stream count, sales and popularity among critics, and fans. As a musician myself I always ask my myself if music is supposed to be subjective, how can the masses like a few particular songs. 

**Is there common factor that make these songs a hit? and if so What are these factors? <br>
  How do our preferences change as time goes by? <br>
  Can we analyze the data to understand why songs go to the top of the charts?** <br>

> Answering these questions might help our target audiences namely music artists and record labels. In this project we will try to answer the question can we group our songs based on it audio properties.      


## Data Dictionary(About the Dataset)

> The dataset is collected from Spotify's API by building a wrapper in Python and extracting relavant information.

> By the end of the collection process, we have a dataset of top 100 songs from 1960 to 2020

> Scale of the dataset:   6077 observation, and 19 variables.

|  Column Name      | Data Type   | Description                                             
| ----------------- | -------------| -------------------------------------------------------
|  billboard_year   | numeric      | Year for the billboard list.    
| song_id           | alphanumeric | Song id as per Spotify.                
| name              | character    | Name of the song
| artist	           | character    | Artist of the song
| release_date	     | datetime     | Release date of the single 
| popularity        | numeric      | A measure of the stream count and downloads for the song on Spotify.
| danceability 	    | numeric      | A measure of danceable is the song.
| energy	           | numeric      | Overall energy of the song.
| key	              | numeric      | Key the song is. key of C is denoted by 0, C# by 1, D by 2 and so on.
| loudness	         | numeric      | The dBs the song is recorded at.
| mode	             | numeric      | measure if song is in Major or Minor scale. 0 is minor and 1 is major. 
| speechiness	      | numeric      | amount of specch pattern present in the song.
| acousticness	     | numeric      | amount of acoustic sound presence in the song.
| instrumentalness	 | numeric      | measure of instruments in the song as opposed to vocals.
| liveness	         | numeric      | Presence of live audience in the track.
| valence	          | numeric      | Value to measure mood of the song. Higher the valence, happier the song mood.
| tempo	            | numeric      | Beats per minute measure for the song.
| duration_ms	      | numeric      | Duration of the track in miliseconds
| time_signature    | numeric      | The time signature of the track. eg 1/4, 3/4 or 4/4 and so on.
