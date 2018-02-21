
# coding: utf-8

# ### Nilanjan Mhatre (801045013)

# In[1]:

import tweepy
import time



ACCESS_TOKEN = '964929660143439873-dH104TJExRHK1KJM4BoaQFaTXHlLClb'
ACCESS_SECRET = 'Ned0SCdZVbEbLEeSMQ0ETmMozTV6Gczd2Fi8vYzgvxTiR'
CONSUMER_KEY = 'zpUK7eFMfe5qY6X7PBvybbf56'
CONSUMER_SECRET = '6o4B0bj2a7xKM9CZzBAbXAziR7l8lEKaUSlLpZyiMyEIlag2RD'
SEARCH = input("Enter the search string ")
FROM = input("Enter the from date (YYYY-MM-DD format) ")
TO = input("Enter the to data (YYYY-MM-DD format) ")
INPUT_FILE_PATH = './'+SEARCH+'.txt'
FILE_ABC = SEARCH+'.txt'

num=int(input("Enter the number of tweets you want to retrieve for the search string "))
n=int(input("Enter the number of max "))
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
i=0;

f = open(INPUT_FILE_PATH, 'w', encoding='utf-8')

#tweets = tweepy.Cursor(api.search, q=SEARCH, rpp=100, count=20, since=FROM, until=TO, lang="en").items(num)
tweets = tweepy.Cursor(api.search, q=("{}&since:{}&until:{}").format(SEARCH,FROM,TO), rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(num)

for res in tweets:
   i+=1
   f.write(res.user.screen_name)
   f.write(' ')
   f.write('[')
   f.write(res.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"))
   f.write(']')    
   f.write(" ")
   f.write('"')
   f.write(res.text.replace('\n', ''))
   f.write('"')
   f.write(" ")
   f.write(str(res.user.followers_count))
   f.write(" ")
   f.write(str(res.retweet_count))
   f.write('\n')
f.close
print("Tweets retrieved ", i)


# In[3]:

import nltk
from nltk import word_tokenize
import pandas as pd
import numpy as np
from datetime import datetime



nltk.download('punkt')



with open(FILE_ABC,encoding='utf8') as f:
    contentData = f.readlines()
    



contentData



tweets = []
for item in contentData:
    temp=[]
    tokens = word_tokenize(item)
    user = tokens[0]
    time = datetime.strptime(tokens[2],"%d/%b/%Y:%H:%M:%S")
    split_data = tokens[2].split(':')
    hour = split_data[1]
    #print(split_row[1])
    #print(tokens[2])
    tweetText = ' '.join(tokens[5:len(tokens)-3])
    followers = int(tokens[len(tokens)-2])
    retweetCount = int(tokens[len(tokens)-1])
    temp.append(user)
    temp.append(time)
    temp.append(tweetText)
    temp.append(followers)
    temp.append(retweetCount)
    temp.append(hour)
    tweets.append(temp)


tweets



tweetsDataframe=pd.DataFrame(tweets, columns=['User', 'Time','TweetText','Followers','RetweetCount','Hour'])
tweetsDataframe


# ### a.    The top n users who have tweeted the most for the entire timeline.


topNUsers = tweetsDataframe['User'].groupby(tweetsDataframe['User']).count().reset_index(name="count")
topNUsers = topNUsers.sort_values(by = 'count',ascending=False).head(n)
topNUsers.to_csv('TopNUsers.csv', sep=',')


# ### b. The top n users who have tweeted the most for every hour.


hours = tweetsDataframe['Hour']
for i in hours:
    topNUserForHour = tweetsDataframe[tweetsDataframe['Hour']==i][['User','Hour']]
    topNUserForHour = topNUserForHour['User'].groupby(topNUserForHour['User']).count().reset_index(name="count")  
    topNUserForHour = topNUserForHour.sort_values(by = 'count',ascending=False)
    topNUserForHour.to_csv('Hour'+i+'.csv',sep=',')


# ### c.    The top n users who have the maximum followers.


topNUserForFollowers = tweetsDataframe.drop(['Time','TweetText','RetweetCount','Hour'],axis=1).sort_values(by='Followers', ascending=False).groupby(tweetsDataframe['User']).head().drop_duplicates().head(n)
topNUserForFollowers.to_csv('topNUserForFollowers.csv', sep=',')


# ### d.    The top n tweets which have the maximum retweet count


topNUserForRetweetCount = tweetsDataframe.drop(['Time','User','Followers','Hour'],axis=1).sort_values(by='RetweetCount', ascending=False).groupby(tweetsDataframe['TweetText']).head().drop_duplicates().head(n)
topNUserForRetweetCount.to_csv('topNUserForRetweetCount.csv', sep=',')