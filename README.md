# Bots Project

This repository will store the data the research team used to analyze tweets related to various topics. The code folder also includes my work analyzing the 2019 Hong Kong protests. Most of the code is Nicolas' (without the twitter credentials file). It is placed here for ease of reference and completeness' sake. 

## Scraping Tweets (Folder 1) 
The first folder contains code to scrape and store tweets in a format compatible with the rest of this repository. This section draws almost completey from [here](https://github.com/NicolasGDM/Query_twitter_data). I made minor changes to fix errors and update the database appropriately. 

Here are some helpful tips for getting started with Nicolas' code:
- Apply for a Twitter developer account! Once you've been approved, go [here](https://developer.twitter.com/en/apps), create an app, click on app details, and generate your keys and tokens
- Install [anaconda](https://www.anaconda.com/distribution/)
- Open anaconda prompt and type: *pip install twython* and *pip install tweepy*
- Fill in the twitter_credentials.py file, but delete all the hashtags at the beginning (so you're left with just four lines of credentials)
- I recommend using search.py. Be sure to change the start_date and end_date variables in the code appropriately. A free developer account only lets you scrape back seven days. The only cost for duplicate tweets or overlapping time ranges is time - the code uses dictionaries which are, by definition, unique. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset"
python search.py twitter_credentials.py hashtags "HK English" hongkong hkprotest hkprotests hongkongprotests hongkongprotest hongkongers
```
- I scraped around one million tweets over the course of 20 days, though my topic was a hot issue on Twitter when I was scraping. For less active topics, scraping a sizeable amount of tweets may take longer. 
- Your .db file contains 7 json files (or python dictionaries): tweet, tweet_hashtags, tweet_media, tweet_url, tweet_usermentions, user, and user_profile. At this point, the database only contains information about tweets. To fill in the user_profile json, use the search_userextraction.py I coded. For around 300,000 users, the code took approximately 50 minutes to run.
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset"
python search_userextraction.py twitter_credentials.py "HK English"
```
- Now, we will export the two json files of interest (tweet and user_profile) from the .db file. They will appear in the same folder your .db file lives in. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset"
python export_tweets_users.py "HK English"
```

## Labeling Tweets (Folder 2) 

1. Come up with your list of keywords for both pro/anti your topic and update the hashtags files in the *labeling* folder. If you are using languages other than english, make sure to use .txt files (rather than .csv) to use the right UTF-8 encoding. [This](https://hashtagify.me/hashtag/tbt) was helpful for finding some of the more popular hashtags for my topic. 

2. Next, we will label your tweets based on whether they include pro/anti keywords. Be sure to change the file path at the top of the code, including the extra "\" at the end of the string.  
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\2. HK Training\labeling"
python label.py
```

## Training the Neural Network (Folder 2) 
