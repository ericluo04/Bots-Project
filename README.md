# Bots Project

This repository will store the data the research team used to analyze tweets related to various topics. The code folder also includes my work analyzing the 2019 Hong Kong protests. Some of the code is a duplicate of Nicolas' code (without the twitter credentials file). It is placed here for ease of reference and completeness' sake. 

## Scraping Tweets (1) 
To scrape and store tweets in a format compatible with the code in this repository, please follow the steps listed [here](https://github.com/NicolasGDM/Query_twitter_data).

Here are some helpful tips for getting started with Nicolas' code:
- Apply for a Twitter developer account! Once you've been approved, go [here](https://developer.twitter.com/en/apps), create an app, click on app details, and generate your keys and tokens
- Install [anaconda](https://www.anaconda.com/distribution/)
- Open anaconda prompt and type: *pip install twython* and *pip install tweepy*
- Fill in the twitter_credentials.py file, but delete all the hashtags at the beginning (so you're left with just four lines of credentials)
- I recommend using search.py. Be sure to change the start_date and end_date variables in the code appropriately. A free developer account only lets you scrape back seven days. The scraping will often time out after 15 minutes, so it may be best practice to run this code (with the updated date ranges) daily to capture as many of the requested tweets as possible within a single session. 
- Below are sample scripts in anaconda prompt to run the code
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset"
python search.py twitter_credentials.py hashtags "HK English" hongkong hkprotest hkprotests hongkongprotests hongkongprotest hongkongers
```
- In your .db file, it contains 7 json files (or python dictionaries): tweet, tweet_hashtags, tweet_media, tweet_url, tweet_usermentions, user, and user_profile. At this point, the database only contains information about tweets; user_profile hasn't been filled in yet. We will need profile descriptions later. To do this step, use the search_userextraction.py I coded. Below are sample scripts in anaconda prompt to run the code
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset"
python search_userextraction.py twitter_credentials.py "HK English"
```

## Labeling Tweets (2) 

1. Your data should be in a .db (SQLite) format. Convert these files to .json using *import_all.py* in the *sqlite-to-json* folder. Change the path variable in the python file. Below are sample scripts in anaconda prompt to run the code. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\2. HK Training\sqlite-to-json"
python import_all.py
```

2. Come up with your list of keywords for both pro/anti your topic and update the hashtags files in the *labeling* folder. If you are using languages other than english, make sure to use .txt files (rather than .csv) to use the right UTF-8 encoding. 

## Training the Neural Network (2) 
