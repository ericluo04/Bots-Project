import json
import pandas as pd

## create input csv file
with open(r"C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset\HK English\user_profile.json") as json_file:
    data = [json.loads(line) for line in json_file]

users = pd.DataFrame.from_dict(data)[['user_id','screen_name',"friends_count","followers_count"]]
users = users.dropna()

users.to_csv('users.csv', index=False, header = None)
