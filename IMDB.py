
# coding: utf-8

# #  IMDB All U.S. Released Movies: 1972-2016 Analysis

# In[50]:

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# ### Creating pandas empty data frame 
# data will be filled after reading url

# In[280]:

columns =['name','year','runtime', 'certificate','genre','rating','url']
mov_df = pd.DataFrame(columns=columns)


# ## Collecting Movie name, year, duration, certificate, genre, rating

# In[282]:

from datetime import datetime
print(str(datetime.now()))
rows = []
for count in range(1,101):
    html = urlopen("http://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page="+str(count))
    bsObj = BeautifulSoup(html.read(), "lxml");
    nameList=bsObj.find_all("div", class_="lister-item-content")
    name=url=certificate=genre = 'None'
    year=runtime=rating=''
    for h in nameList:
        name = h.find('a').text
        if h.find('span',class_="lister-item-year text-muted unbold") is not None:
            year = h.find('span',class_="lister-item-year text-muted unbold").text
        if h.find('span',class_="runtime") is not None:
            runtime = h.find('span',class_="runtime").text
        if h.find('div',class_="inline-block ratings-imdb-rating") is not None:
            if 'data-value' in h.find('div',class_="inline-block ratings-imdb-rating").attrs.keys():
                rating = h.find('div',class_="inline-block ratings-imdb-rating").attrs['data-value']
        url = h.find('a').attrs['href']
        if h.find('span',class_="certificate") is not None:
            certificate = h.find('span',class_="certificate").text
        if h.find('span',class_="genre") is not None:
            genre = h.find('span',class_="genre").text
        row=[name,year,runtime,certificate,genre.strip(' \t\n\r'),rating,'http://www.imdb.com'+url.split("?",1)[0]]
        rows.append(row)
        
        
df = pd.DataFrame(rows, columns=columns)
   
print(str(datetime.now()))
print(df.head(5))


# ##  Persisting data

# In[283]:

df.to_csv('IMDB_Movie_List.csv')


# ## Collecting Parental guide info for collected movies

# * column for Movie Id so that we can join later

# In[370]:

df['movie_id'] = df.url.str[-10:-1]
print(df.head())


# ###  Creating 5x4 variable to store paraental guidance 
# Each movies is reviewed under five catogeries
# * Sex & Nudity
# * Violence & Gore
# * Profanity 
# * Alcohol, Drugs & Smoking
# * Frightening & Intense Scenes
# 
# 
# 
# Under Each Categoriy user has four levels to rate the movies
# * None
# * Mild
# * Moderat
# * Severe

# In[360]:

p_columns =['movie_id','nudity','nudity_none','nudity_mild','nudity_moderate','nudity_severe',
        'violence','violence_none','violence_mild','violence_moderate','violence_severe',
        'profanity','profanity_none','profanity_mild','profanity_moderate','profanity_severe',
        'alcohol','alcohol_none','alcohol_mild','alcohol_moderate','alcohol_severe',
        'frightening','frightening_none','frightening_mild','frightening_moderate','frightening_severe']


# In[367]:

couter=len(df)


# #### Get Parents Guide data 

# In[369]:

print(str(datetime.now()))
p_rows = []
for i in range(0,couter):
    movie_id = df['movie_id'][i]
    p_url=df['url'][i]+'parentalguide'
    p_html = urlopen(p_url)
    p_bsObj = BeautifulSoup(p_html.read(), "lxml")
    p_nameList=p_bsObj.find_all("section",class_='article listo content-advisories-index')
    nudity_none=nudity_mild=nudity_moderate=nudity_severe=0
    violence_none=violence_mild=violence_moderate=violence_severe=0
    profanity_none=profanity_mild=profanity_moderate=profanity_severe=0
    alcohol_none=alcohol_mild=alcohol_moderate=alcohol_severe=0
    frightening_none=frightening_mild=frightening_moderate=frightening_severe=0
    nudity=violence=profanity=alcohol=frightening=''
    for h in p_nameList:
        til = h.find_all('section')

        for p in til:
            
            A_None=Mild=Moderate=Severe=0
            if not (p.get('id') == 'certificates'  or 'spoiler' in p.get('id')) :
                advisory=p.find('h4').text
                if p.find('span',class_='advisory-severity-vote__vote-button-container') is not None:
                    strArr=p.find('span',class_='advisory-severity-vote__vote-button-container').text.splitlines()
                    str_list = list(filter(None, strArr))
                    none=str_list[1]
                    mild=str_list[3]
                    moderate=str_list[5]
                    severe=str_list[7]
                if p.find('div',class_='advisory-severity-vote__container ipl-zebra-list__item') is not None:
                    strArr=p.find('div',class_='advisory-severity-vote__container ipl-zebra-list__item').text.splitlines()
                    str_list = list(filter(None, strArr))
                    temp_advisory=str_list[0]
                
                if advisory =='Sex & Nudity':
                    nudity = temp_advisory
                    nudity_none=none
                    nudity_mild=mild
                    nudity_moderate=moderate
                    nudity_severe=severe
                    
                elif advisory == 'Violence & Gore':
                    violence = temp_advisory
                    violence_none=none
                    violence_mild=mild
                    violence_moderate=moderate
                    violence_severe=severe
                    
                elif advisory == 'Profanity':
                    profanity = temp_advisory
                    profanity_none=none
                    profanity_mild=mild
                    profanity_moderate = moderate
                    profanity_severe=severe
                elif advisory == 'Alcohol, Drugs & Smoking':
                    alcohol = temp_advisory
                    alcohol_none=none
                    alcohol_mild=mild
                    alcohol_moderate=moderate
                    alcohol_severe=severe
                elif advisory == 'Frightening & Intense Scenes':
                    frightening = temp_advisory
                    frightening_none=none
                    frightening_mild=mild
                    frightening_moderate=moderate
                    frightening_severe=severe
                
            
    row=(movie_id,nudity,nudity_none,nudity_mild,nudity_moderate,nudity_severe,
        violence,violence_none,violence_mild,violence_moderate,violence_severe,
        profanity,profanity_none,profanity_mild,profanity_moderate,profanity_severe,
        alcohol,alcohol_none,alcohol_mild,alcohol_moderate,alcohol_severe,
        frightening,frightening_none,frightening_mild,frightening_moderate,frightening_severe)
    p_rows.append(row)
    


p_df = pd.DataFrame(p_rows, columns=p_columns)
   
print(str(datetime.now()))
print(p_df.head(5))

p_df.to_csv('Movie_PG.csv')    




# ## Maerge both dataframe

# In[372]:

final_df=pd.merge(df, p_df, on='movie_id', how='outer')
final_df.to_csv('IMDB_Complete_data.csv')    
final_df.head(5)


# ## Next : Get Plot Keywords data and merge with above data

# In[277]:

keywords_url=new_df['url'][0]+'keywords'
print(keywords_url)
 


# In[278]:

keywords_html = urlopen(keywords_url)
keywords_bsObj = BeautifulSoup(keywords_html.read(), "lxml");

