#!/usr/bin/env python
# coding: utf-8

# <h1><center> Anatomy of a song </center></h1>
# <h2><center> Analyzing Billboard Hot 100 from 1960 to 2020 </center></h2>
# 
# 
# ### Introduction
# From the first week of December to the final week of November, Billboard runs a year-end chart giving us the highest performing songs for a given year. The year-end charts are calculated by a very straightforward cumulative total of yearlong sales, streaming, and airplay points which gives a more accurate picture of any given year's most popular tracks. Thanks to to Spotify's API we can get data for these all these songs and analyze them to get a clear picture of an anatomy of a popular song. 
# 
# A small caveat before we begin, Billboard only accounts for sales and streaming in the US. So these songs are popular with respect to only the United States of America. Also as a musician myself, I cannot stress enough the subjectivity of music. Every person in this world has a right to love any type of music and this list only reflects songs which made more sales and were popular in broader spectrum. 

# ### Methodology
# ####  Data Collection
# 
# To collect the data, Spotify has been generous enough to provide us developers with a robust API. So I built a wrapper class in Python that would get me songs, albums, playlists and audio properties of the songs from the API. 
# 
# First step was to collect the playlist ids, for the playlists on spotify which had a complied list of year-end top 100 songs. Using those ids, I got the respective song ids of every song in that playlist. Second step was to use these song ids to extract audio properties and metadata for each song in the playlists. 
# 
# Finnaly we have a data with about 7000 songs, and 19 variables across 50 years.

# In[43]:


#importing all necessary libraries
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from pandas.core.groupby.groupby import GroupBy
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import matplotlib.pyplot as plt
import seaborn as sns


# In[35]:


df = pd.read_csv(r"C:\Users\phadk\Desktop\Work\projects\portfolio\Spotify_eda\data.csv")
data = df.drop_duplicates(subset=['song_id', 'billboard_year'])
data.head(5)


# #### Exploratory Data Analysis
# 
# The core of any analysis projects lies in asking the right questions. Before I collected the data these were the few questions that I hoped to answer at the end of the notebook.
# 
# ###### 1. How long does an artist stay relevant or popular?
# 
# In music we have terms called influential artists or timeless performers. Artists like The Beatles, Micheal Jackson, Madonna, Tupak Shakur and many more are still relevant and still loved by the people today. Obviously most of these artists don't stay on billboard chart forever as sales go down as other artists take over. But to stay on billboard charts for years on speaks to how much an artist can stay popular across generations.

# In[48]:


top_artists = data.groupby(["artist"]).size().reset_index(name="Count").sort_values(by='Count',ascending=False).head(50)
plt.figure(figsize=(16, 16))
sns.barplot(x="Count", y="artist", data=top_artists,palette="Blues_d")


# We see that after we start going towards right of the chart, every artist same almost the same amount of songs making the billboard list but the artists at the left have put out a considerable amount of singles every year. But to understand their true influence on the industry we must look also look at for how many years have they consistenly dominated the charts. 

# In[131]:


top_25 = data[data['artist'].isin(list(top_artists['artist'])[0:25])]
ctdf= top_25.groupby('artist').billboard_year.agg(['max','min']).reset_index()
ctdf['min'] = pd.to_datetime(ctdf['min'], format='%Y').dt.year
ctdf['max'] = pd.to_datetime(ctdf['max'], format='%Y').dt.year
ctdf = ctdf.rename(columns={"artist": "Task", "min": "Start","max":"Finish"})
fig = ff.create_gantt(ctdf)
iplot(fig)


# One important conclusion from these graph proves that having most charting singles does not necessarily correlate to career longetivity. For example Micheal Jackson ruled the chart from 1970 to early 2014. So how did the king of pop span a sucessfull career for almost 4 decades? was it only his brand name, or did he always keep evolving his music style, with current trends or is there a secret formula that almost always work, which brings us to my next question.    

# ###### Do the top charting songs change according to time, or have common elements?
# 
# All the songs in our dataset had certain amount of infulence over sales, popularity among the people and positive praise from the critics. While music is subective to the listener there are a few elements in music that define its greatness. Another very importnat factor is current trend. While rock and roll was the talk of the town in the 60s, Hip hop and rap ruled the charts 40 years later with almost no rock & roll track on the charts. We can do this with looking at audio properties of a songs, Lets start by 4 factor that drive the songs personality the most.
# 
# 1. Dancebility : Dscribes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.
# > Think : Sexy back by Justin Timberlake or almost any song by James Brown.
# 
# 2. Acousticness: A measure from 0.0 to 1.0 of whether the track has acoustic elements.
# > Think : Cant help falling in love with you by Elvis Presley
# 
# 3. Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.
# > Think of how much energy artists like Spice girls, Prince, Bon Jovi or micheal Jackson bring in their performances.  
# 
# 4. Instrumentalness: Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.
# > Examples like Sir Elton John, or Ludwig van Beethoven or Chopin

# In[25]:


data1 = data.groupby('billboard_year', group_keys=False).apply(pd.DataFrame.sample, frac=.1)


# In[76]:


g= sns.lmplot(data=data1,x="billboard_year", y="danceability",palette="rocket",height=5)
g.fig.set_size_inches(15,5)


# In[66]:


g= sns.lmplot(
    data=data1,
    x="billboard_year", y="acousticness",
    height=5
)
g.fig.set_size_inches(15,5)


# In[67]:


g= sns.lmplot(
    data=data1,
    x="billboard_year", y="instrumentalness",
    height=5
)
g.fig.set_size_inches(15,5)


# In[69]:


g= sns.lmplot(
    data=data1,
    x="billboard_year", y="energy",
    height=5
)
g.fig.set_size_inches(15,5)


# In these scatter plots we see dancebility and energy has had steady growth while acousticness has had a sharp decline. Another thing we notice is that instrumentalness is consistently low. Let's chart the histogram of all these values to get a better understanding.

# In[105]:


plt.figure(figsize=(16, 4))
plt.subplot(1, 2, 1)  # 1 line, 2 rows, index nr 1 (first position in the subplot)
plt.hist(data['danceability'])
plt.subplot(1, 2, 2)  # 1 line, 2 rows, index nr 2 (second position in the subplot)
plt.hist(data['acousticness'])
plt.show()

plt.figure(figsize=(16, 8))
plt.subplot(2, 2, 1)  # 1 line, 2 rows, index nr 2 (second position in the subplot)
plt.hist(data['energy'])
plt.subplot(2, 2, 2)  # 1 line, 2 rows, index nr 2 (second position in the subplot)
plt.hist(data['instrumentalness'])
plt.show()


# This confirms our scatter plots. We see acousticness has very sharp decline. This can attribute to technological advances in sound engineering. Bands in the 60s and early 70s had to rely a lot on their mastery over the instruments but as time passed music produciton played a vital role in music. When artist saw that the could produce entire songs only with the help studio effects, natural sounds(which contribute to acousticness) reduced. Hence the sharp decline. This new tech can also explain the increase in energy quotient of a track and its danceability. Just look at how hip-hop and EDM music's infulence on the early 2000s. 
# 
# When comes to instrumentelness its consistently low across all decades hence pointing to possible common element. Now if billboard and spotify were arround the 1800s or early 1920s we might just see a different outcome. So sorry, Mr Bach you are not gonna sell much of those beautiful classical pieces in the 21st century.
# 
# 

# After looking at the properties we would want to look at the duration of song.

# In[143]:


data['duration_min'] = data['duration_ms']/60000
g = sns.jointplot(y=data['duration_min'], x=data['billboard_year'], color="blue")
g.fig.set_size_inches(15,7)


# It is quite clear that all the top charting songs lasted for about 5 minutes irrespective of their release year. So this is definately a common element between different top track across decades

# Another important factor in decoding the personality of the song is its complexity to the listener.To gauge complexity of a song the time signature variable is a great feature. 

# In[113]:


ts = data.groupby(["time_signature"]).size().reset_index(name="Count")
plt.figure(figsize=(16, 8))
sns.barplot(x="time_signature", y="Count", data=ts,palette=['red','green','blue','yellow'])


# It is quite clear the time signature 4/4 is the most used among almost all the songs. Now 4/4 time signature is also the most used in music due to its extreme simplicity for reading, composing and performing music. Due to its natural and common occurence the human ears can sounds in this time signature much more easily. 

# One last factor to analyze commonalities, we will look at mood of the song. A mood of the song can be deciphered using two features :
# 
# 1. Mode: Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
# 
# 
# 2. Valence: Valence measure the value of positive, The higher the value, the more positive mood for the song.

# In[120]:


#pie chart for mode
mode = data.groupby(["mode"]).size().reset_index(name="Count")

plt.figure(figsize=(16, 8))
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
plt.pie(mode['Count'], explode=explode, labels=['Minor','Major'], autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# In[124]:


plt.figure(figsize=(16, 8))
plt.hist(data['valence'])


# The last two plots suggests that there is no pattern when it comes to the mood of the song but almost 70% of the song are built in a major key. The reason for major chords sounding "happy" is the something to do with intervals as explained by music theory. Wider intervals are perceived as being brighter than smaller intervals. So major chords with their major 3rd are brighter that minor chords with their minor third. But then if 70% songs have a major chords, why is the valence not distrubuted more towards higher ranges. That is because of another element in our song, pitch. According to several music theorist and pschologists Lower pitches tend to send more bright and happy. Let's look at our pitch or key variable in a pie chart

# In[128]:


#pie chart for key
keys = data.groupby(["key"]).size().reset_index(name="Count")
plt.figure(figsize=(16, 8))
labels = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
plt.pie(keys['Count'], labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# Now here we see that all songs are evenly distrubuted as per their pitches, which explains the incongruency in Mode and valence. 

# #### Conclusion
# 
# While we have only scratched the surface of music analysis, we did see some interesting things with our data that can answer our questions.
# 
# ##### Commanalities 
# > Simplicity: With a time signature of 4/4 almost 90% of these songs feel natural to the listener and hence are listened more.
# 
# > Presence of Vocals: If we neglect the outliers in every year, most of the top charting songs, have heavy presence of vocals.
# 
# > The Major lift : Major chords tend to appeal more to listeners due to the bright,happy and uplifting nature and hence are listened to more.
# 
# ##### Trends
# > Effect of Technology : With advances in sound engineering, composers can rely less on the natural sounds and more on track production effects.
# 
# > Groove it: All the top songs across tend more towards, higher danceability but the subtle nuances in them speak about how our culture around dance forms has changed.
# 
# 

# 
# 
# 
# <center><b>While we see that there are countless exteral factors that might affect the career of an artist, to stay relevant in the industry and a musician must adapt and evolve to match current compitition. This right to change or staying true to a style remains solely with the artist. Afterall music is art and it's beauty lies in ears of the beholder</center><b>

# In[ ]:




