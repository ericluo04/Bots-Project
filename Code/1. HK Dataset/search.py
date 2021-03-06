# -*- coding: UTF-8 -*-
from twython import Twython
from datetime import datetime, timedelta
import numpy as np
from helper import *
import sqlite3
from operator import itemgetter
import sys 
import os

credentials=sys.argv[1]
mode = sys.argv[2]
db=sys.argv[3]
target = sys.argv[4:]

if not os.path.exists(db):
    os.makedirs('./'+db)

conn = sqlite3.connect('./'+db+'/'+db+'.db')
c = conn.cursor()


############################################################
####################### Your credentials ###################
############################################################
with open(credentials) as f:
    lines = f.read().splitlines()
twitter = Twython(*lines)



#####################################################################################
####################### Will create sqlite tables the first time  ###################
#####################################################################################
create_tables(c,conn)
create_tweet_tables(c,conn)





#################################################################
####################### Pick start/end dates ###################
################################################################

####### NOTE : if you want you can query the DB for the most recent date, or most recent tweet id, in order not to search again for previous tweets.
####### That is useful if you want to Crontab the queries on engaging for like a week. I did that once, if you're unfamiliar with sqlite queries from python ask me =)


#### TIME RECORD:
#### 1. 9/16-9/19 (86,814 tweets)
#### 2. 9/19-9/22 (380,193) tweets)
#### 3. 9/23-9/29 (157,748) tweets)
### 4. 9/30-10/3 (142,512 tweets)
### 5. 9/30-10/3 (471,028 "chinese" tweets - likely picked up on english, japanese, and korean as well)
### 6. 9/30-10/1 (364,244 tweets)
### 7. 10/2-10/8 (485,432 tweets)
### 8. 10/9-10/11 (855,808 tweets)
### 9. 10/11-10/15
### 10. 10/16-10/23
### 11. 10/24-10/26
### 12. 10/27-11/3
### 13. 1/1-1/7
### 14. 1/12-1/19
### 15. 1/22-1/29
### 15. 1/29-2/6
### 16. 2/9-2/16
today=datetime.now()
today=datetime(today.year,today.month,today.day,0,0,0)
start_date = datetime(year=2020, month=2, day=9) # or you can pick start_date = today
end_date = start_date + timedelta(days=7) # or you can pick another end_date 
earliestTweet=0 # or you can pick latest tweet from previous query
latestTweet=-1


#####################################
########## Query a hashtag ##########
#####################################
if(mode == 'hashtags'):
	input_list_of_target_hashtags = target 
	print('Start inserting timelines in database')
	queryAndInsertTweetsContainingHashtag(twitter, input_list_of_target_hashtags, start_date, end_date, earliestTweet, latestTweet, 10000000,conn,c,today)

#########################################
######## Query a user_timeline ##########
#########################################

elif(mode == 'users'): ##remember to authentificate as oauth2 for higher API limits
	new_tweets = []
	target_users = [int(i) for i in target]
	print('Start querying timelines')
	count=0
	for user in target_users:
		count+=1
		print('Now querying tweets of user ', user, ' number ', count, ' on ', len(target_users))
		counter= queryAndInsertUsersTimelines(twitter,c,conn,user)
		print('Got ', counter, ' new tweets from user')
		print('Done querying user ', user)
	
	print('Done querying timelines')
	
	print('Now querying profiles of people')
	queryAndInsertUsersProfiles(twitter, c, conn, today, target_users)

	##few line below do the same but should be slower
	# new_users = queryUsersProfiles(twitter, target_users)
	# print('Start inserting user profiles in database')
	# insertUserProfiles(c,conn,new_users,today,today)


elif(mode=='location'):
	getAndInsertTweetsWithPicsByLocation(twitter,start_date, end_date, earliestTweet, latestTweet, 10000000, conn, c, today)

