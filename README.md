# Bots Project

This repository will store the data the research team used to analyze tweets related to various topics. The code folder also includes my work analyzing the 2019 Hong Kong protests.

## Scraping Tweets (Folder 1) 
The first folder contains code to scrape and store tweets in a format compatible with the rest of this repository. This section draws almost completey from [here](https://github.com/NicolasGDM/Query_twitter_data). I made minor changes to fix errors and update the database appropriately. 

Here are some helpful tips for getting started with Nicolas' code:
1. Apply for a Twitter developer account! Once you've been approved, go [here](https://developer.twitter.com/en/apps), create an app, click on app details, and generate your keys and tokens
2. Install [anaconda](https://www.anaconda.com/distribution/)
3. Open anaconda prompt and type: *pip install twython* and *pip install tweepy*
4. Fill in the twitter_credentials.py file, but delete all the hashtags at the beginning (so you're left with just four lines of credentials)
5. I recommend using search.py. Be sure to change the start_date and end_date variables in the code appropriately. A free developer account only lets you scrape back seven days. The only cost for duplicate tweets or overlapping time ranges is time - the code uses dictionaries which are, by definition, unique. I scraped around one million tweets over the course of 20 days, though my topic was a hot issue on Twitter when I was scraping. For less active topics, scraping a sizeable amount of tweets may take longer. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\1. HK Dataset"
python search.py twitter_credentials.py hashtags "HK English" hongkong hkprotest hkprotests hongkongprotests hongkongprotest hongkongers
```
7. Your .db file contains 7 json files (or python dictionaries): tweet, tweet_hashtags, tweet_media, tweet_url, tweet_usermentions, user, and user_profile. At this point, the database only contains information about tweets. To fill in the user_profile json, use the search_userextraction.py I coded. For around 300,000 users, the code took approximately 50 minutes to run.
```
python search_userextraction.py twitter_credentials.py "HK English"
```
8. Now, we will export the two json files of interest (tweet and user_profile) from the .db file. They will appear in the same folder your .db file lives in. 
```
python export_tweets_users.py "HK English"
```
9. If necessary, remove tweets with duplicate text values. Duplication could occur when multiple users retweet the same tweet or when activists copy and paste messages. Change the path file variable first. 
```
python no_dups_tweets.py
```

#### Summary Statistics:
Number of Tweets: 2,334,689  
Number of Users: 523,646  
Number of Unique Tweets: 414,963  

## Labeling Tweets (Folder 2) 

1. Come up with your list of keywords for both pro/anti your topic and update the hashtags files in the *labeling* folder. If you are using languages other than english, make sure to use .txt files (rather than .csv) to use the right UTF-8 encoding. [This](https://hashtagify.me/hashtag/tbt) was helpful for finding some of the more popular hashtags for my topic. 
2. Next, we will label your tweets based on whether they include pro/anti keywords. Be sure to change the file path at the top of the code, including the extra "\\" at the end of the string.  
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\2. HK Training\labeling"
python label.py
```
3. Balance your labeled tweets so that the number of pro and anti tweets are the same. 
```
python balance.py
```

#### Summary Statistics:
Before Balancing:
- Anti: 7.00% (12,100)
- Pro: 93.00% (160,704)

After Balancing:
- Anti: 50% (12,100)
- Pro: 50% (12,100)

*Note:* This labeling process is extremely context dependent - carefully study your issue's rhetoric on Twitter to craft a representative list of pro and anti hashtags that can reliably reveal one's signal on your issue. With the Hong Kong protests, the discourse on Twitter leans heavily towards pro-Hong Kong. To increase the training samples on the pro-China side, I include several broad hashtags that may have introduced some noise (e.g. riot, riots, rioter, rioters, mob, mobs, thug, thugs). However, given the nature of discussion on the Hong Kong issue, the assumption that these hashtags can expose a pro-China account seems reasonable. Otherwise, I would have had only 3,487 pro-China training examples. Especially with NLP tools, more data is generally preferred, despite the possibility of a more noisy sample [(Banko and Brill, 2001)](https://www.aclweb.org/anthology/P01-1005.pdf).

## Training the Neural Network (Folder 2) 
1. Put the *labeled_data_balanced.csv* file in the Training>Data folder and rename it to *modeling_1.csv*.
2. Now, train the CNN LSTM model. Take note of the seq_len value, which is hardcoded later in the get_polarity.py code. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\2. HK Training\training"
python train.py
```
3. Move your dictionaries from training>Dictionary to polarities>Dictionary. Replace the new weights in polarities>Final_weights and rename them to *final_weights.hdf5*. Change the seq_len value in model.py and helper_text.py (the main_clean function near the bottom). Now, run the code below to extract user polarities. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\2. HK Training\polarities"
python get_polarity.py
```
4. Extract tweet-level polarities. This will be the "master file." You can access previous master files from various topics [here](https://drive.google.com/drive/u/0/folders/11y8ULyX0mLi9vp-1_Ofz3EvN8rFRdl6U). 
```
python master_polarity.py
```
#### Summary Statistics:
- test set accuracy:  1.0
- base line accuracy:  1.0
- seq_len:  18

## Bots (Folder 3) 
1. Build the friends graph. The code for this is in *Scraping_Hacks*. First, create a .csv file with user information from your database: user_id, screen_name, friends_count, and followers_count. Next, build the graph. The first number represents the batch number (starting at 1); the second number, the batch size; and the third number, the maximum number of friends before requesting the API. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\3. HK Bots\Scraping_Hacks"
python users_CSV.py
python twitter_friends_graph_script.py "users.csv" 1 10000 3000
```
2. Build the retweet graph. First, create a .csv file with information about retweet interactions between users in your database. 
```
cd "C:\Users\ericluo04\Documents\GitHub\Bots-Project\Code\3. HK Bots"
python retweetCSV.py
```
