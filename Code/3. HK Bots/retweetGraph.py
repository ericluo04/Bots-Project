import json
import re
import pandas as pd

# CHANGE THIS FILE PATH
with open(r"C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset\HK English\tweet.json") as json_file:
    data = [json.loads(line) for line in json_file]     # read in json of tweets as a dictionary

# create new dictionary key with screen name of retweeted user
for i in range(len(data)):
    screen_name = re.search("RT @([\w]*):", data[i]['text'])
    if screen_name != None:
        data[i]['retweet_screen_name'] = screen_name.group(1)
    else:
        data[i]['retweet_screen_name'] = None

# create pandas dataframe for scalability
hkdf = pd.DataFrame.from_dict(data)[['user_id','screen_name','retweet_screen_name']]
hkdf = hkdf.dropna()

# create dictionary of users inside database with a userID
userdict = pd.Series(hkdf.user_id.values, index=hkdf.screen_name).to_dict()

# only include retweeted users if already inside the database with a userID
hkdf["retweet_user_id"] = hkdf["retweet_screen_name"].map(userdict)
hkdf_short = hkdf.dropna()

# group by number of retweet interactions between users
hkdf_forcsvoutput = hkdf_short.groupby(hkdf_short.columns.tolist()).size().reset_index().\
    rename(columns={0:'num_retweets'}).sort_values(['num_retweets'], ascending=[True])

# save three columns of interest
hkdf_forcsvoutput = hkdf_forcsvoutput[['user_id', 'retweet_user_id', 'num_retweets']]

# expot
hkdf_forcsvoutput.to_csv('testTweetsoutput.csv',index=False)
