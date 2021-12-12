import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    return cur, conn

def bar_one(cur):
    cur.execute("SELECT Crypto.name, Tweets.tweet_count from Tweets JOIN Crypto ON Tweets.id = Crypto.crypto_id")
    data = cur.fetchall()
    
    xlist = [tup[0] for tup in data]
    ylist = [tup[1] for tup in data]

    plt.bar(xlist, ylist, color = "blue")
    plt.xlabel("Crypto Name")
    plt.ylabel("Number of Tweets")
    plt.title("Number of Tweets for Cryptocurrencies")
    plt.xticks(rotation=90)

    plt.show()

def scatter_one(cur):
    cur.execute("SELECT Tweets.tweet_count, Crypto.percent_change_24h from Tweets JOIN Crypto ON Tweets.id = Crypto.crypto_id")
    data = cur.fetchall()
    
    xlist = [tup[0] for tup in data]
    ylist = [tup[1] for tup in data]

    fig, ax = plt.subplots()
    ax.scatter(xlist, ylist, color = "orange")
    ax.set_xticks(np.arange(0, 12000, 500))
    ax.set_xlim(0, 1500) # gets rid of outliers 
    plt.xlabel("Tweet Count")
    plt.ylabel("Percentage Increase over 24 Hours")
    plt.title("Percentage of Price Increase for Cryptocurrency over 24 Hours vs Number of Times the Cryptocurrency was Mentioned on Twitter")
    plt.show()
    #discuss outliers


# Create a scatter chart vizualization using matplotlib with the data returned from Combined table
def scatter_two(cur):
    cur.execute("SELECT Tweets.tweet_count, Crypto.percent_change_7d from Tweets JOIN Crypto ON Tweets.id = Crypto.crypto_id")
    data = cur.fetchall()
    
    xlist = [tup[0] for tup in data]
    ylist = [tup[1] for tup in data]

    fig, ax = plt.subplots()
    ax.scatter(xlist, ylist, color = "blue")
    ax.set_xticks(np.arange(0, 11000, 500))
    ax.set_xlim(0, 5000) # gets rid of outliers 
    plt.xlabel("Tweet Count")
    plt.ylabel("Percentage Increase over 7 days")
    plt.title("Percentage of Price Increase for Cryptocurrency over 7 Days vs Number of Times the Cryptocurrency was Mentioned on Twitter")
    plt.show()

def main():

    cur,conn = setUpDatabase('crypto.db') 
    bar_one(cur)
    scatter_one(cur)
    scatter_two(cur)

    conn.close()

if __name__ == "__main__":
    main()
