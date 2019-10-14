# -*- coding: UTF-8 -*-
from twython import Twython
from datetime import datetime, timedelta
import numpy as np
from helper import *
import sqlite3
from operator import itemgetter
import sys 
import os
import json

credentials=sys.argv[1]
db = sys.argv[2]

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

# gets all tweets from the database
def get_all_users( json_str = False ):
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from tweet
    ''').fetchall()

    #conn.commit()
    #conn.close()

    if json_str:
        return [dict(ix) for ix in rows] #CREATE JSON

    return rows

twtdata = get_all_users(json_str = True)


#####################################
######## Query user profiles ########
#####################################
today=datetime.now()

print('Now querying profiles of people that posted the tweets')
queryAndInsertUsersProfilesThatPostedTheTweets(twitter, c, conn, today, twtdata)
