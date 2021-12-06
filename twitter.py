# Twitter File
from bs4 import BeautifulSoup
import requests
import json
import tweepy 
import sqlite3          
import os

consumer_key = "tv6h21bxvLZe4EfUKb6jEOngO"
consumer_secret = "xHwJCd0Km4JqjxxzJlgfPYMtkbMGKvKQVdQfZb7hQYcMddRMGP"
access_token = "2967918434-PBT2EGFDYnhEABVox00z6hk8zxlbkIO1kmO48uy"
access_token_secret = "gWltdO8LBAfOtfv7X5s3BZvnhCpKkpisJAZD4q3taQqgh"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPV4VwEAAAAABNBqe8IOkS6pIaOf%2Fn65R%2BH00k0%3DEAttM3EYnstTxcHXx2mNzrapL6g1xMQYbZVumRriagVMXDXtS4"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type= dict)
# consumer_key = "tv6h21bxvLZe4EfUKb6jEOngO"
# consumer_secret = "xHwJCd0Km4JqjxxzJlgfPYMtkbMGKvKQVdQfZb7hQYcMddRMGP"
# access_token = "2967918434-PBT2EGFDYnhEABVox00z6hk8zxlbkIO1kmO48uy"
# access_token_secret = "gWltdO8LBAfOtfv7X5s3BZvnhCpKkpisJAZD4q3taQqgh"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, timeout=1200, parser=tweepy.parsers.JSONParser(), wait_on_rate_limit=True, retry_count=3)

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAAPV4VwEAAAAABNBqe8IOkS6pIaOf%2Fn65R%2BH00k0%3DEAttM3EYnstTxcHXx2mNzrapL6g1xMQYbZVumRriagVMXDXtS4")

# search_url = "https://api.twitter.com/2/tweets/counts/recent"

# # Optional params: start_time,end_time,since_id,until_id,next_token,granularity
# query_params = {'query': 'from:twitterdev','granularity': 'day'}


# def bearer_oauth(r):
#     """
#     Method required by bearer token authentication.
#     """

#     r.headers["Authorization"] = f"Bearer {bearer_token}"
#     r.headers["User-Agent"] = "v2RecentTweetCountsPython"
#     return r


# def connect_to_endpoint(url, params):
#     response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
#     print(response.status_code)
#     if response.status_code != 200:
#         raise Exception(response.status_code, response.text)
#     return response.json()


# def main():
#     json_response = connect_to_endpoint(search_url, query_params)
#     print(json.dumps(json_response, indent=4, sort_keys=True))


# if __name__ == "__main__":
#     main()

def getTweets():
    # using beautiful soup to get data from the Top Grossing Movies of 2019
    base_url = 'https://api.twitter.com/1.1/search/tweets.json?q=from%3Aelonmusk%20%23bitcoin&result_type=popular'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    

def create_twitter_table():
    """Takes in the database cursor and connection as inputs. Returns nothing. Creates Twitter_Data table. 
    Uses the Movie_Title column from the MovieChart_2019 table to find tweets containing the movie title. 
    Adds number of favorites per search, followers, number of mentions, retweets, friends count, listed count, and statuses count per search for each of the movies."""
   
    # cur.execute("CREATE TABLE IF NOT EXISTS Twitter_Data (Twitter_Id INTEGER UNIQUE, Movie_Title TEXT UNIQUE, Movie_Mentions INTEGER, Movie_Favorited INTEGER, Follower_Count INTEGER, Retweet INTEGER, Friends_Count INTEGER, Listed_Count INTEGER, Statuses_Count INTEGER, PRIMARY KEY(Twitter_Id AUTOINCREMENT))")
    
    # # grab movie titles from the MovieChart_2019 table
    # cur.execute('SELECT Movie_Title FROM MovieChart_2019')
    # movie_list = cur.fetchall()

    # # grab movie titles from the Twitter_Data
    # cur.execute('SELECT Movie_Title FROM Twitter_Data')
    # movie_names = cur.fetchall()

    # # empty list for the movies 
    # existing_movies = []

    # # add name from Twitter_Data into the list and find the length of the list
    # for name in movie_names:
    #     existing_movies.append(name[0])
    # key = len(movie_names)

    crypto_list = ['bitcoin', 'ethereum', 'solana']
    # goes through the mvoies from MovieChart_2019
    for crypto in crypto_list:
    #     crypto = crypto[0]

        # search for the movie in Twitter and grab the results from the search
        results = api.search_recent_tweets(query=crypto)
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
        
        
        print(results)

#         # put the data into the Twitter_Data table
#         # cur.execute("INSERT OR IGNORE INTO Twitter_Data (Twitter_Id, Movie_Title, Movie_Mentions, Movie_Favorited, Follower_Count, Retweet, Friends_Count, Listed_Count, Statuses_Count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
#         # (crypto, mentions_count, favorite_count, follower_count, retweet_count, friends_count, listed_count, statuses_count))
 
#     # conn.commit()
#     # status = soup.findall("statuses")
#     # print(status)

# # def setUpDatabase(con, cur):
# #     """Takes in the database cursor and connection as inputs. Returns nothing. Creates Twitter_Data table. 
# #     Uses the crypto_name column from the crypto_chart table to find tweets mentioning the cryptocurrency name."""
# #     cur.execute("CREATE TABLE IF NOT EXISTS Twitter_Data (twitter_id INTEGER UNIQUE, crypto_name TEXT UNIQUE, PRIMARY KEY(twitter_id AUTOINCREMENT))")
    
# #     # grab crypto names from the crypto_chart table
# #     cur.execute('SELECT crypto_name FROM crypto_chart')
# #     crypto_list = cur.fetchall()

# #     # grab crypto names from the Twitter_Data
# #     cur.execute('SELECT crypto_name FROM Twitter_Data')
# #     crypto_names = cur.fetchall()

# #     # empty list for cryptos
# #     crypto_list = []

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
#     Calls the functions created_tables(), set_up_genre_id_table(), set_up_date_id_table(), 
#     set_up_distributor_id_table(), fillup_table(), and write_data_to_file(). Closes the database connection."""
#     # getTweets()
     create_twitter_table()
#     # cur, conn = setUpDatabase('movies.db')
#     # created_tables(cur, conn)
#     # set_up_genre_id_table(cur, conn)
#     # set_up_date_id_table(cur, conn)
#     # set_up_distributor_id_table(cur,conn)
#     # fillup_table(cur, conn)
#     # write_data_to_file("movie_data.txt", cur, conn)
#     # conn.close()

if __name__ == "__main__":
    main()