import json
import re
import pandas as pd
import pickle

# CHANGE PATH ACCORDINGLY
path = "C:/Users/ericluo04/Documents/GitHub/Bots-Project/Code/"

# open up tweet json file
with open(path + "1. HK Dataset/HK English/tweet_nodups.json") as json_file:
    data = [json.loads(line) for line in json_file]

# create new key value for retweeted screen name if tweet is a retweet
for i in range(len(data)):
    screen_name = re.search("RT @([\w]*):", data[i]['text'])
    if screen_name != None:
        data[i]['retweet_screen_name'] = screen_name.group(1)
    else:
        data[i]['retweet_screen_name'] = None

# convert to pandas
hkdf = pd.DataFrame.from_dict(data)[['user_id','screen_name','retweet_screen_name']]
hkdf = hkdf.dropna()

# create users dictionary, only include retweet interactions among users in database
userdict = pd.Series(hkdf.user_id.values, index=hkdf.screen_name).to_dict()
hkdf["retweet_user_id"] = hkdf["retweet_screen_name"].map(userdict)
hkdf_short = hkdf.dropna()

# create desired retweet graph csv format
hkdf_forcsvoutput = hkdf_short.groupby(hkdf_short.columns.tolist()).size().reset_index().\
    rename(columns={0:'num_retweets'}).sort_values(['num_retweets'], ascending=[True])

# save columns of interest and export as csv
hkdf_forcsvoutput = hkdf_forcsvoutput[['user_id', 'retweet_user_id', 'num_retweets']]
hkdf_forcsvoutput.to_csv(path + "3. HK Bots/RT_graphs/HKProtests_G0_RT_GRAPH.csv", index=False, header=False, sep=';')
