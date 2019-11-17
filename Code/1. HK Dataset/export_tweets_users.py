# -*- coding: UTF-8 -*-
import numpy as np
from helper import *
import sqlite3
from operator import itemgetter
import sys 
import os
import json

db=sys.argv[1]

if not os.path.exists(db):
    os.makedirs('./'+db)

conn = sqlite3.connect('./'+db+'/'+db+'.db')
c = conn.cursor()

#####################################################################################
####################### Will create sqlite tables the first time  ###################
#####################################################################################
create_tables(c,conn)
create_tweet_tables(c,conn)

# gets all tweets from the database
# merge with user_profiles to get user description information as well
def get_all_tweets( json_str = False ):
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute('''
    SELECT A.tweet_id, A.user_id, A.screen_name, A.created_at, A.text, A.lang, B.description
    FROM tweet A
    LEFT JOIN user_profile B on A.user_id = B.user_id
    ''').fetchall()

    conn.commit()
    
    if json_str:
        return [dict(ix) for ix in rows] #CREATE JSON

    return rows

twtdata = get_all_tweets(json_str = True)

print("Your database has " + str(len(twtdata)) + " tweets.")

# save tweets as json file
with open('./'+ db + '/tweet.json', 'w') as outfile:
    for tweet in twtdata:
        json.dump(tweet, outfile)
        outfile.write('\n')


# gets all user profiles from the database
def get_all_users( json_str = False ):
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute('''
    SELECT *
    from user_profile
    ''').fetchall()

    if json_str:
        return [dict(ix) for ix in rows] #CREATE JSON

    return rows

userdata = get_all_users(json_str = True)

print("Your database has " + str(len(userdata)) + " users.")

# save user profiles as json file
with open('./'+ db + '/user_profile.json', 'w') as outfile:
    for user in userdata:
        json.dump(user, outfile)
        outfile.write('\n')
