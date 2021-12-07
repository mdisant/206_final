# Twitter File
from bs4 import BeautifulSoup
import requests
import json
import tweepy 
import sqlite3          
import os
import re

# consumer_key = "tv6h21bxvLZe4EfUKb6jEOngO"
# consumer_secret = "xHwJCd0Km4JqjxxzJlgfPYMtkbMGKvKQVdQfZb7hQYcMddRMGP"
# access_token = "2967918434-PBT2EGFDYnhEABVox00z6hk8zxlbkIO1kmO48uy"
# access_token_secret = "gWltdO8LBAfOtfv7X5s3BZvnhCpKkpisJAZD4q3taQqgh"
# bearer_token = "AAAAAAAAAAAAAAAAAAAAAPV4VwEAAAAABNBqe8IOkS6pIaOf%2Fn65R%2BH00k0%3DEAttM3EYnstTxcHXx2mNzrapL6g1xMQYbZVumRriagVMXDXtS4"

consumer_key = "TfyjYQDGNhNm7KOuQa2JQUZ6x"
consumer_secret = "5YetECIama1can1SwkRmEaXBmTz8KnXofqImlOH7Pfbb0IFEbO"
access_token = "1400081139361013762-qJFq7xtQ4viWUNwN33tFtF5D8vIAdu"
access_token_secret = "aYN0nlJqEfp86Yk24S1U7q65eePt3OlyW9hbesX15eveZ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANtPWgEAAAAAkoStv0CJRLz57bfTtfMgLgWOx1w%3DOejMKa67emE79o4sBWHJbolAPvRr0uGsCff1AcMOK13NmZpBtE"

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

        results_list = results['data']
        for dict in results_list:
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

def combined_data(cur):
    cur.execute("SELECT * FROM Tweets JOIN Crypto ON Tweets.crypto = Crypto.name")
    data = cur.fetchall()
    return data

def make_combined_table(data, cur, conn):
    cur.execute("DROP TABLE IF EXISTS Combined")
    cur.execute("CREATE TABLE IF NOT EXISTS Combined (crypto_name TEXT PRIMARY KEY, count INTEGER, increase_24h REAL, increase_7d REAL)")
    
    for tup in data:

        cur.execute("INSERT OR IGNORE INTO Combined (crypto_name,count, increase_24h, increase_7d) VALUES (?,?,?,?)",(tup[0], tup[3], tup[8], tup[9]))
    
    conn.commit()


def main():

    cur,conn = setUpDatabase('crypto.db')
    result = create_twitter_tuple(cur, conn)

    setUpTweetsTable(result, cur, conn)
    combined = combined_data(cur)
    make_combined_table(combined, cur, conn)

    conn.close()

if __name__ == "__main__":
    main()