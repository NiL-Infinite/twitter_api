'''
Created on Feb 17, 2018

@author: nilan
'''

import tweepy
import time
from pip.index import Search
import nltk
import pandas as pd
import numpy as np
from datetime import datetime
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')

ACCESS_TOKEN = '964929660143439873-dH104TJExRHK1KJM4BoaQFaTXHlLClb'
ACCESS_SECRET = 'Ned0SCdZVbEbLEeSMQ0ETmMozTV6Gczd2Fi8vYzgvxTiR'
CONSUMER_KEY = 'LqmguwFU22tkiaTjPXpDbGknM'
CONSUMER_SECRET = 'j5G9GPfx1jOx1iEKrDJL4pujtZAvYOrkRxxvZCh8KyHj9G1jvQ'
SEARCH = input("Enter the search string ")
FROM = input("Enter the from date (YYYY-MM-DD format) ")
TO = input("Enter the to data (YYYY-MM-DD format) ")
INPUT_FILE_PATH = './'+SEARCH+'.txt'

num=int(input("Enter the number of tweets you want to retrieve for the search string "))
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
i=0;

f = open(INPUT_FILE_PATH, 'w', encoding='utf-8')

tweets = tweepy.Cursor(api.search, q=SEARCH, since = FROM, until =TO, rpp=100, count=20, result_type="recent", include_entities=True, lang="en")


for tweet in tweets.items():
    i+=1
    f.write(tweet.user.screen_name)
    f.write(' ')
    f.write('[')
    f.write(tweet.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"))
    f.write(']')    
    f.write(" ")
    f.write('"')
    f.write(tweet.text.replace('\n', ''))
    f.write('"')
    f.write(" ")
    f.write(str(tweet.user.followers_count))
    f.write(" ")
    f.write(str(tweet.retweet_count))
    f.write('\n')
f.close
print("Tweets retrieved ", i)



with open(INPUT_FILE_PATH,encoding='utf8') as f:
    content = f.readlines()

tweets = []
for item in content:
    temp=[]
    tokens = word_tokenize(item)
    username = tokens[0]
    createdAt = datetime.strptime(tokens[2],"%d/%b/%Y:%H:%M:%S")
    split_row = tokens[2].split(':')
    hour = split_row[1]
    text = ' '.join(tokens[5:len(tokens)-3])
    followers = int(tokens[len(tokens)-2])
    retweetCount = int(tokens[len(tokens)-1])
    temp.append(username)
    temp.append(createdAt)
    temp.append(text)
    temp.append(followers)
    temp.append(retweetCount)
    temp.append(hour)
    tweets.append(temp)



tweetsDataframe=pd.DataFrame(tweets, columns=['username', 'createdAt','text','followers','retweetCount','hour'])
#tweetsDataframe = tweetsDataframe.sort_values(by=['createdAt'],ascending=True)


# In[89]:


tweetsDataframe.head()


# In[90]:


#Top n users who have tweeted the most related to the search string for the entire timeline
userCount = tweetsDataframe['username'].groupby(tweetsDataframe['username']).count().reset_index(name="count")
userCount = userCount.sort_values(by = 'count',ascending=False)
userCount = userCount

userCount.to_csv('MostTweetedUsers.csv', sep=',')


#Top n users who have tweeted the most for every hour
hours = tweetsDataframe['hour']
for i in hours:
    
    topEveryHour = tweetsDataframe[tweetsDataframe['hour']==i][['username','hour']]
    topEveryHour = topEveryHour['username'].groupby(topEveryHour['username']).count().reset_index(name="count")
    topEveryHour.to_csv('Hour'+i+'.csv',sep=',')

topEveryHour = tweetsDataframe[tweetsDataframe['hour']=='05'][['username', 'hour']]



#The top n users who have the maximum followers.
userCount = tweetsDataframe.drop(columns=['createdAt','text','retweetCount','hour'], axis=1).sort_values(by='followers', ascending=False).groupby(tweetsDataframe['username']).head().drop_duplicates()

userCount.to_csv('MostFollowerUsers.csv', sep=',')




#The top n tweets which have the maximum retweet count.
userCount = tweetsDataframe.drop(columns=['createdAt','username','followers','hour'], axis=1).sort_values(by='retweetCount', ascending=False).groupby(tweetsDataframe['text']).head().drop_duplicates()

userCount.to_csv('MaxRetweetCountUsers.csv', sep=',')

