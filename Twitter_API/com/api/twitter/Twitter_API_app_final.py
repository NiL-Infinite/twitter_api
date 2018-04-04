
# coding: utf-8

# ### Nilanjan Mhatre (801045013)

# In[1]:

import tweepy
import time
import csv
from operator import itemgetter
from collections import OrderedDict
from unittest.test.testmock.testpatch import function



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
from datetime import datetime, timedelta



nltk.download('punkt')



with open(FILE_ABC,encoding='utf8') as f:
    contentData = f.readlines()
    



tweets = []
for item in contentData:
    temp=[]
    tokens = word_tokenize(item)
    user = tokens[0]
    time = datetime.strptime(tokens[2],"%d/%b/%Y:%H:%M:%S")
    tweetText = ' '.join(tokens[5:len(tokens)-3])
    try:
        followers = int(tokens[len(tokens)-2])
    except ValueError:
        followers = 0
    try:
        retweetCount = int(tokens[len(tokens)-1])
    except ValueError:
        retweetCount = 0
    temp.append(user)
    temp.append(time)
    temp.append(tweetText)
    temp.append(followers)
    temp.append(retweetCount)
    tweets.append(temp)


def sortTweets(tweetsList):
    tweetsUserCount = {}

    for tweet in tweetsList:
        if (tweet[0] in tweetsUserCount):
            tweetCount = tweetsUserCount.get(tweet[0])
            tweetsUserCount[tweet[0]] = tweetCount + 1
        else:
            tweetsUserCount[tweet[0]] = 1
        sortedUsers = sorted(tweetsUserCount.items(), key=itemgetter(1), reverse=True)
    return sortedUsers


# ### a.    The top n users who have tweeted the most for the entire timeline.
# tweetsUserCount = {}
# 
# for tweet in tweets:
#     if (tweet[0] in tweetsUserCount):
#         tweetCount = tweetsUserCount.get(tweet[0])
#         tweetsUserCount[tweet[0]] = tweetCount + 1
#     else:
#         tweetsUserCount[tweet[0]] = 1
# 
# sortedUsers = sorted(tweetsUserCount.items(), key=itemgetter(1), reverse=True)
sortedUsers = sortTweets(tweets)
with open('top_N_users_max_tweets.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['User', 'Tweet Count'])
    tempCount = 0;
    for key, value in sortedUsers:
        if (tempCount < n):
            filewriter.writerow([key, value])
        tempCount = tempCount + 1



# ### b. The top n users who have tweeted the most for every hour.

currentTime = datetime.strptime(FROM,"%Y-%m-%d")
toTime = datetime.strptime(TO,"%Y-%m-%d") + timedelta(days=1)

with open('per_hour_top_N_users_max_tweets.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['From', 'To'])
    while currentTime <= toTime:
        endTime = currentTime + timedelta(seconds=3600)
        filteredTweets = [t for t in tweets if t[1] <= endTime and t[1] >= currentTime]
        filewriter.writerow([currentTime, endTime])
        if len(filteredTweets) > 0:
            sortedUsers = sortTweets(filteredTweets)
            tempCount = 0;
            for key, value in sortedUsers:
                if (tempCount < n):
                    filewriter.writerow(['', key, value])
                tempCount = tempCount + 1

        currentTime = endTime
        


# ### c.    The top n users who have the maximum followers.
tweetsFollowersCount = {}

for tweet in tweets:
    if (tweet[0] in tweetsFollowersCount):
        tweetCount = tweetsFollowersCount.get(tweet[0])
        tweetsFollowersCount[tweet[0]] = tweetCount + tweet[3]
    else:
        tweetsFollowersCount[tweet[0]] = tweet[3]

sortedUsers = sorted(tweetsFollowersCount.items(), key=itemgetter(1), reverse=True)
print(sortedUsers)

with open('top_N_users_max_followers.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['User', 'Followers'])
    tempCount = 0;
    for key, value in sortedUsers:
        if (tempCount < n):
            filewriter.writerow([key, value])
        tempCount = tempCount + 1




# ### d.    The top n tweets which have the maximum retweet count

sortedTweets = sorted(tweets, key=itemgetter(4), reverse=True)
print(sortedTweets)

with open('top_N_retweets_tweets.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['User', 'Retweet Count'])
    tempCount = 0;
    for tweet in sortedTweets:
        if (tempCount < n):
            filewriter.writerow([tweet[0], tweet[4]])
        tempCount = tempCount + 1

