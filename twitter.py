# Twitter File
from bs4 import BeautifulSoup
import requests
import json
import tweepy 
import sqlite3          
import os
import re

consumer_key = "tv6h21bxvLZe4EfUKb6jEOngO"
consumer_secret = "xHwJCd0Km4JqjxxzJlgfPYMtkbMGKvKQVdQfZb7hQYcMddRMGP"
access_token = "2967918434-PBT2EGFDYnhEABVox00z6hk8zxlbkIO1kmO48uy"
access_token_secret = "gWltdO8LBAfOtfv7X5s3BZvnhCpKkpisJAZD4q3taQqgh"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPV4VwEAAAAABNBqe8IOkS6pIaOf%2Fn65R%2BH00k0%3DEAttM3EYnstTxcHXx2mNzrapL6g1xMQYbZVumRriagVMXDXtS4"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type= dict)
    

def create_twitter_tuple(cur, conn):
    
    # grab crypto names from the Crypto table
    cur.execute('SELECT name FROM Crypto')
    crypto_list = cur.fetchall()
    # prepare to strip text of emojis etc. 
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    crypto_key_list = [1, 52, 74, 825, 1027, 1839, 2010, 3408, 3635, 3890, 4172, 5426, 5805, 5994, 6636]
    tuple_list = []
    # goes through the cryptos from Crypto table
    for crypto in crypto_list:

        # search for the crypto in Twitter and grab the results from the search
        results = api.search_recent_tweets(query=crypto, max_results = 25)
        tweet_id_list = []
        text_list = []
        key_list = []
        favorites_list = []
        followers_list = []
        retweets_list = []
        results_list = results['data']
        for dict in results_list:
            tweet_id_list.append(dict['id'])
            text_stripped = dict['text'].replace('/n', ' ')
            text_demoji = emoji_pattern.sub(r'', text_stripped)
            text_list.append(text_demoji)
            # key_list.append(key)
            tuple_list.append((crypto[0], dict['id'], text_demoji))
        

        # count = api.get_recent_tweet_count(query=crypto)
        retweet_count = 0
        mentions_count = 0
        favorite_count = 0
        follower_count = 0
        friends_count  = 0
        listed_count = 0
        statuses_count = 0

        # for all of the results, grab the favorite_count and retweet_count of the movie. 
        # also grab the followers_count, friends_count, listed_count, and statuses_count of the user that mentioned the movie
        # for result in results['statuses']:
            # fav_count = result['favorite_count']
            # favorite_count += fav_count
            # tweet_count = result['retweet_count']
            # retweet_count += tweet_count
            # fol_count = result['user']['followers_count']
            # follower_count += fol_count
            # friend_count = result['user']['friends_count']
            # friends_count += friend_count
            # list_count =  result['user']['listed_count']
            # listed_count += list_count
            # status_count = result['user']['statuses_count']
            # statuses_count += status_count
            # mentions_count += 1
        # print(tweet_id_list)
        # print(text_list)
        # print(key_list)
    print(tuple_list)
    return tuple_list

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    # pass name in main function

# 3 cols, primary id (which crypto), tweet id, and text

def setUpTweetsTable(tupleslist, cur, conn):

    # loop through bigger dict first, value to data key is list of dicts
    # nested for loop
    cur.execute("DROP TABLE Tweets")
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (crypto TEXT PRIMARY KEY, tweet_id INTEGER UNIQUE, text TEXT)")
    count = 0
    
    # ensures 25 entries at a time, run code 4 times
    for tup in tupleslist:
        if count == 25:
            break
        cur.execute("INSERT OR IGNORE INTO Tweets (crypto, tweet_id, text) VALUES (?,?, ?)",(tup[0], tup[1], tup[2]))
        if cur.rowcount == 1:
            count += 1
    conn.commit()

    

        # put the data into the Twitter_Data table
        # cur.execute("INSERT OR IGNORE INTO Twitter_Data (Twitter_Id, Movie_Title, Movie_Mentions, Movie_Favorited, Follower_Count, Retweet, Friends_Count, Listed_Count, Statuses_Count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        # (crypto, mentions_count, favorite_count, follower_count, retweet_count, friends_count, listed_count, statuses_count))
 
    # conn.commit()
    # status = soup.findall("statuses")
    # print(status)

# def setUpDatabase(con, cur):
#     """Takes in the database cursor and connection as inputs. Returns nothing. Creates Twitter_Data table. 
#     Uses the crypto_name column from the crypto_chart table to find tweets mentioning the cryptocurrency name."""
#     cur.execute("CREATE TABLE IF NOT EXISTS Twitter_Data (twitter_id INTEGER UNIQUE, crypto_name TEXT UNIQUE, PRIMARY KEY(twitter_id AUTOINCREMENT))")
    
#     # grab crypto names from the crypto_chart table
#     cur.execute('SELECT crypto_name FROM crypto_chart')
#     crypto_list = cur.fetchall()

#     # grab crypto names from the Twitter_Data
#     cur.execute('SELECT crypto_name FROM Twitter_Data')
#     crypto_names = cur.fetchall()

#     # empty list for cryptos
#     crypto_list = []

# # def setUpCategoriesTable(data, cur, conn):
# #     category_list = []
# #     for business in data['businesses']:
# #         business_categories = business['categories']
# #         for category in business_categories:
# #             if category['title'] not in category_list:
# #                 category_list.append(category['title'])

# #     cur.execute("DROP TABLE IF EXISTS Categories")
# #     cur.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, title TEXT)")
# #     for i in range(len(category_list)):
# #         cur.execute("INSERT INTO Categories (id,title) VALUES (?,?)",(i,category_list[i]))
# #     conn.commit()


def main():
#     """Takes nothing as an input and returns nothing. 

    cur,conn = setUpDatabase('crypto.db')
    result = create_twitter_tuple(cur, conn)

    setUpTweetsTable(result, cur, conn)

    conn.close()

if __name__ == "__main__":
    main()