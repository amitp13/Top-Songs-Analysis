# Top-Songs-Analysis

## Problem Statement

> Every songs has its personality, For example Fire and Rain by James Taylor is a nice acoustic song for easy listening, while nirvana's smells like teen spirit is full of energy and teenage angst. Then we have songs to dance to like, shape of you by Ed Sheeran.
 <br>

> A few questions arise, <br>
**Is there common factor that make these songs a hit? and if so What are these factors? <br>
  How do our preferences change as time goes by? <br>
  Can we analyze the data to understand why songs go to the top of the charts?** <br>

> Answering these questions might help our target audiences namely music artists and record labels. In this project we will try to answer the question can we group our songs based on it audio properties.


## Data Dictionary(About the Dataset)

> The dataset we will be using for the project is sourced from Kaggle. It consits of the top tracks of every year since in 2010 from Billboard.com

> The songs have some basic attributes such as Name, Artist Name, Release Year and Genre. Some important attributes that follow are a few music properties curated by Spotify. The properties include Dancebility, Valence, Energy, Beats Per Minute etc.

> In Summary, the Dataset conatains 15 columns which include the song metadata and its audio properties. A total of 604 songs have been collected since the year 2011 which are a part of the top tracks list of Billboard.com. A detailed description of the feilds is given below.

|  Column Name      | Data Type | Description                                             
| ----------------- | --------- | -------------------------------------------------------
| title             | numeric   | Name of the Song	                                     
| artist	          | character | Artist                                                
| acousiveness      |	numeric   | Acousticness - A confidence measure from 0.0 to 1.0 of whether the track is acoustic.
| dancebility	      | numeric   | Danceability- Describes how suitable a track is for<br>dancing based on a combination of musical elements.
| duration	        | numeric   | Duration - The duration of the track in milliseconds.
| energy            | numeric   | Energy - A measure from 0.0 to 1.0 and represents<br> a perceptual measure of intensity and activity.
| instrumentalness  | numeric   | How much instrumentatility is present in the song.
| liveness	        | numeric   | Liveness - Detects the presence of an audience in the recording.
| loudness	        | numeric   | Loudness - The overall loudness of a track in decibels (dB).
| speechiness       |	numeric   | Speechiness - Speechiness detects the presence of spoken words in a track.
| tempo             | numeric   | tempo of a song
| valence	          | numeric   | Valence - A measure from 0.0 to 1.0 describing the musical positiveness
| pop               | numeric   | Popularity- The higher the value the more popular the song is.
| key               | numeric   | key of the song
| mode              | binary    | mood of a song. 0 or 1 values.

### Contributors :
**Apurva Sarode<br>
Renuka Madhugiri<br>
Amit Phadke<br>**
