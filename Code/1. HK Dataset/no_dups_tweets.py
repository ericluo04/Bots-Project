import json
import re
import pandas as pd

# CHANGE PATH ACCORDINGLY
path = "C:/Users/ericluo04/Documents/GitHub/Bots-Project/Code/"

# open up tweet json file
with open(path + "1. HK Dataset/HK English/tweet.json") as json_file:
    data = [json.loads(line) for line in json_file]

no_dups = pd.DataFrame.from_dict(data)
#dropping all rows with duplicate tweets
no_dups.drop_duplicates(subset = "text", keep = False, inplace = True)

# convert to appropriate dictionary format
no_json = no_dups.to_dict('records')

# save tweets with no text duplicates as json file
count = 0
with open(path + '1. HK Dataset/HK English/' + 'tweet_nodups.json', 'w') as outfile:
    for tweet in no_json:
        json.dump(tweet, outfile)
        outfile.write('\n')
        count+=1
        
print("Number of unique tweets: " + str(count))
