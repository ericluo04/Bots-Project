#!/usr/bin/env python
# coding: utf-8

#upload libraries
import pandas as pd
import numpy as np
import json
from os import listdir
from os.path import isfile, join
from itertools import islice
import re
import progressbar

# In[1]:
from helper_text import main_clean
from model import load_model

model = load_model()

#get list of files in our directory so we can loop through them 

path = "C:/Users/ericluo04/Documents/GitHub/Bots-Project/Code/1. HK Dataset/HK English/"
all_files = [f for f in listdir(path) if isfile(join(path, f))]

print('files are: ', all_files)

#define dictionary where users are keys 
tweet_id =dict()
count = 0. #to track how many batches of data we visited 

# index 1 for with duplicates, index 2 for without
int_files = [all_files[2]] #choose the files we want to mine through
print('files used: ', int_files)

def update(tweet_id, tweets):
    '''
    takes as input:
    tweet_id: dictionary where keys are tweet_id and values are the user's information and polarity
    tweets: dictionary of tweets as available in The Hard Drive 
    Output:
    tweet_id: Update the tweet_id dictionary entered with new information from the tweets data input
    '''
    bar = progressbar.ProgressBar()
    for twt in bar(tweets):
        id_ = twt['tweet_id']
        u = dict()
        # tweet level info
        u['id'] = id_
        u['tweet'] = twt['text']
        u['language'] = twt['lang']
        u['created_at'] = twt['created_at']
        # user level info
        u['user_id'] = twt['user_id']
        u['name'] = twt['name']
        u['screen_name'] = twt['screen_name']
        u['description'] = twt['description']
        u['location'] = twt['location']
        # user level statistics
        u['n_followers'] = twt['followers_count']
        u['n_friends'] = twt['friends_count']
        u['n_tweets_user'] = twt['statuses_count']
        
        x, x_s = main_clean(twt['text'])
        p = model.predict([x, x_s])[:,1][0]
        u['polarity'] = p

        tweet_id[id_] = u
    return(tweet_id)

for file in int_files:
    path_file = path + file
    n = 5000  # Or whatever chunk size you want
    with open(path_file, 'r') as f:
        for tweets in iter(lambda: list(islice((json.loads(line) for line in f), n)), []):
            tweet_id = update(tweet_id, tweets)
            print(len(tweet_id))
            count += 1
            #save every 10 chunks of data (This is just a precaution in case of memory failure, we would have saved something)
            if count % 10 == 0:
                file_name = 'polarities_checkpoint/master_polarities_' + str(len(tweet_id)) + '.npy'
                np.save(file_name, tweet_id)
print('number of tweets in total: ', len(tweet_id))

#save final file
file_name = 'polarities_checkpoint/master_polarities_' + str(len(tweet_id)) + '.npy'
np.save(file_name, tweet_id)

master_file = pd.DataFrame.from_dict(tweet_id).T
#dropping all rows with duplicate tweets
master_file.drop_duplicates(subset = "tweet", keep = False, inplace = True)

# deal with excel row limitations
rowlimit = 1048576
if len(master_file.index) < rowlimit:
    master_file.to_csv('master_new.csv')
elif len(master_file.index) < 2 * rowlimit:
    #split dataframe into 2 to deal with row size limitations in excel
    master1, master2 = np.array_split(master_file, 2)
    #save as csv
    master1.to_csv('master_new_1.csv')
    master2.to_csv('master_new_2.csv')
else:
    #split dataframe into 3 to deal with row size limitations in excel
    master1, master2, master3 = np.array_split(master_file, 3)
    #save as csv
    master1.to_csv('master_new_1.csv')
    master2.to_csv('master_new_2.csv')
    master3.to_csv('master_new_3.csv')
