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

    tuple_list = []
    # goes through the cryptos from Crypto table
    for crypto in crypto_list:

        # search for the crypto in Twitter and grab the results from the search
        results = api.get_recent_tweets_count(query=crypto)
        # start_list = []
        # end_list = []
        # count_list = []

        results_list = results['data']
        for dict in results_list:
            # start_list.append(dict["start"])
            # end_list.append(dict["end"])
            # count_list.append(dict["tweet_count"])
            tuple_list.append((crypto[0], dict["start"], dict["end"], dict["tweet_count"]))
    
    return tuple_list

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    return cur, conn

# 3 cols, primary id (which crypto), tweet id, and text

def setUpTweetsTable(tupleslist, cur, conn):

    cur.execute("DROP TABLE IF EXISTS Tweets")
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (crypto TEXT PRIMARY KEY, start TEXT, end TEXT, count  INTEGER)")
    
    # ensures 25 entries at a time, run code 4 times
    for tup in tupleslist:

        cur.execute("INSERT OR IGNORE INTO Tweets (crypto, start, end, count) VALUES (?,?,?,?)",(tup[0], tup[1], tup[2], tup[3]))
    
    conn.commit()

def main():

    cur,conn = setUpDatabase('crypto.db')
    result = create_twitter_tuple(cur, conn)

    setUpTweetsTable(result, cur, conn)

    conn.close()

if __name__ == "__main__":
    main()