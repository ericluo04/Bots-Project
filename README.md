# Bots Project

## Scraping Tweets
To scrape and store tweets in a format compatible with the code in this repository, please follow the steps listed [here](https://github.com/NicolasGDM/Query_twitter_data).

Here are some helpful tips for getting started with Nicolas' code:
- Apply for a Twitter developer account! Once you've been approved, go [here](https://developer.twitter.com/en/apps), create an app, click on app details, and generate keys and tokens
- install [anaconda](https://www.anaconda.com/distribution/)
- open anaconda prompt and type: "pip install twython" and "pip install tweepy"
- fill in the twitter_credentials.py file, but delete all the hashtags at the beginning (so you're left with just four lines of credentials)
- I recommend using search.py. Be sure to change the start_date and end_date variables in the code appropriately. A free developer account only lets you scrape back seven days, so run this code (with the updated date ranges) weekly. 
- Below are sample scripts in anaconda prompt I used to scrape tweets
```
cd "C:\Users\ericluo04\Desktop\Yale Files\2019-2020 Files of Yale\S&DS 491\1. HK Dataset\Query_twitter_data-master"
python search.py twitter_credentials.py hashtags "HK English" hongkong hkProtest hkprotests HongKongProtests hongkongprotest HongKongers
```
