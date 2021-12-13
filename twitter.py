# Twitter File
from bs4 import BeautifulSoup
import requests
import json
import tweepy 
import sqlite3          
import os
import re
import numpy as np

consumer_key = "TfyjYQDGNhNm7KOuQa2JQUZ6x"
consumer_secret = "5YetECIama1can1SwkRmEaXBmTz8KnXofqImlOH7Pfbb0IFEbO"
access_token = "1400081139361013762-qJFq7xtQ4viWUNwN33tFtF5D8vIAdu"
access_token_secret = "aYN0nlJqEfp86Yk24S1U7q65eePt3OlyW9hbesX15eveZ"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANtPWgEAAAAAkoStv0CJRLz57bfTtfMgLgWOx1w%3DOejMKa67emE79o4sBWHJbolAPvRr0uGsCff1AcMOK13NmZpBtE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type= dict)
    
def create_twitter_tuple(cur):
    cur.execute('SELECT name, crypto_id FROM Crypto')
    crypto_list = cur.fetchall()

    tuple_list = []
    for crypto in crypto_list:
        results = api.get_recent_tweets_count(query=crypto[0])

        results_list = results['data']
        for dict in results_list:
            tuple_list.append((crypto[1], dict["tweet_count"]))
    
    return tuple_list

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    return cur, conn

def setUpTweetsTable(tuple_list, cur, conn):
    # cur.execute("DROP TABLE IF EXISTS Tweets")
    cur.execute("CREATE TABLE IF NOT EXISTS Tweets (id INTEGER PRIMARY KEY, tweet_count INTEGER)")
    count = 0
    
    for tup in tuple_list:
        if count == 25:
             break
        cur.execute("INSERT OR IGNORE INTO Tweets (id, tweet_count) VALUES (?,?)",(tup[0], tup[1]))
        if cur.rowcount == 1:
             count += 1
    conn.commit()

def calculate_correlation(cur, timeline):
    cur.execute(f"SELECT Tweets.tweet_count, Crypto.{timeline} from Tweets JOIN Crypto ON Tweets.id = Crypto.crypto_id")
    corr_data = cur.fetchall()

    xlist = [tup[0] for tup in corr_data]
    ylist = [tup[1] for tup in corr_data]

    x_avg = sum(xlist) / len(xlist)
    y_avg = sum(ylist) / len(ylist)

    cor_numerator = 0
    cor_x_denominator = 0
    cor_y_denominator = 0

    for i in range(len(xlist)):
        x_dif = xlist[i] - x_avg
        y_dif = ylist[i] - y_avg
        
        cor_numerator += x_dif * y_dif
        cor_x_denominator += x_dif ** 2
        cor_y_denominator += y_dif ** 2

    corr = cor_numerator / np.sqrt(cor_x_denominator * cor_y_denominator)
    return round(corr, 5)

def write_out_data(fname, cur):
    correlation_24h = calculate_correlation(cur, "percent_change_7d")
    correlation_7d = calculate_correlation(cur, "percent_change_24h")

    with open(fname, "w") as f:
        f.write(f"The calculated Pearson Correlation Coefficient between number of Tweets and percent change in the past 24 hours is:\n{correlation_24h}\n")
        f.write("\n")
        f.write(f"The calculated Pearson Correlation Coefficient between number of Tweets and percent change in the past 7 days is:\n{correlation_7d}\n")



def main():
    cur,conn = setUpDatabase('crypto.db')

    result = create_twitter_tuple(cur)
    setUpTweetsTable(result, cur, conn)

    write_out_data("twitter.txt", cur)

    conn.close()

if __name__ == "__main__":
    main()