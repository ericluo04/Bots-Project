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
import csv
import os


path = "/Users/ericluo04/Documents/GitHub/Bots-Project/Code/1. HK Dataset/HK English/"

# In[17]:
#seperate tweets into their users
def seperate(tweets):
    '''
    takes as input tweets and seperate them into their own users 
    return a dictionary with keys as user ids and values as description and all tweets of this user in input tweets
    '''
    users = dict()
    bar = progressbar.ProgressBar()
    for twt in bar(tweets):
        id_ = twt['user_id']
        try:
            users[id_]['tweets'].append(twt['text'])
        except:
            u = dict()
            #this user does not exist
            u['description'] = twt['description']
            u['tweets'] = [twt['text']]
            users[id_] = u
    return(users)

#keywords for pro your topic
hash_pro = list(pd.read_csv("hashtags_pro.txt", sep = ",", names= ['hashtag'], encoding='utf-8').hashtag)
#hash_pro = [''.join(re.findall('[0-9A-Za-z]', hash_pro[i])) for i in range(len(hash_pro))]
keywords_pro = '|'.join(hash_pro)

#keywords for anti your topic
hash_anti = list(pd.read_csv("hashtags_anti.txt", sep = ",", names= ['hashtag'], encoding='utf-8').hashtag)
#hash_anti = [''.join(re.findall('[0-9A-Za-z]', hash_anti[i])) for i in range(len(hash_anti))]
keywords_anti = '|'.join(hash_anti) #for regex 


def pro_or_anti(description):
    if bool(re.search(keywords_pro, description, re.IGNORECASE)):
        return(0)
    elif bool(re.search(keywords_anti, description, re.IGNORECASE)):
        return(1)
    else:
        return(None)

def pro_anti(users):
    #list of pro, anti tweets
    pro = []
    anti = []
    bar = progressbar.ProgressBar()
    for usr in bar(users.keys()):
        description = str(users[usr]['tweets'])
        #print(description)
        #see if pro/anti/None
        ind = pro_or_anti(description)
        if ind == 1: #anti
            anti.extend(list(users[usr]['tweets']))
        elif ind == 0: #pro
            pro.extend(list(users[usr]['tweets']))
        else:
            pass
    return(pro, anti)



#get list of files in our directory so we can loop through them 
all_files = [f for f in listdir(path) if isfile(join(path, f))]
if '.DS_Store' in all_files:
    all_files.remove('.DS_Store')

print('files are: ', all_files)


#create csv where we will store data

with open('Data/labeled_tweets.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #wr.writerow(['index', 'tweet', 'label'])




def get_data(int_files, n_max, party = None):
    count = 0
    n_tweets = 0
    for file in int_files:
        path_file = path + file
        n = 5000  # Or whatever chunk size you want
        with open(path_file, 'r') as f:
            pro, anti = [], []
            for tweets in iter(lambda: list(islice((json.loads(line) for line in f), n)), []):
                users = seperate(tweets)
                pro_, anti_ = pro_anti(users) #this gives us a list of pro and anti tweets
                pro.extend(pro_)
                anti.extend(anti_)
                count += 1
                #save every 10 chunks of data (i.e. 50000 tweets)
                if count % 1 == 0:
                    pro = [[i, 0] for i in pro_]
                    anti = [[i, 1] for i in anti_]
                    if party == 'pro':
                        all_ = pro
                    elif party == 'anti':
                        all_ = anti
                    else:
                        all_ = pro + anti
                    df = pd.DataFrame(all_, columns = ['tweet', 'pro/anti'])
                    n_tweets += df.shape[0]
                    print(n_tweets)
                    #print(df.head(10))
                    with open('Data/labeled_tweets.csv', 'a',  encoding = 'utf-8', newline='') as f_data:
                        file_is_empty = os.stat('Data/labeled_tweets.csv').st_size == 0
                        if file_is_empty:
                            df.to_csv(f_data, header=True)
                        else:
                            df.to_csv(f_data, header=False)
                if n_tweets > n_max:  
                    print('stop: maximum number of tweets reached')
                    break

n_max = 10000000000 #max_number of tweets
int_files = [all_files[1]]
get_data(int_files, n_max)
