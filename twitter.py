# Twitter File
from bs4 import BeautifulSoup
import requests
import json
import tweepy 
import sqlite3          
import os

api_key = "Ml21tyrWwvCnMJpM77eMThon2"
api_secret_key = "0p196npwcCTw6FsfSbFhy3HOws1gEGEYwpOrHwKZ0gGBrQBuiy"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPV4VwEAAAAAA12jk9BOokvmURj4aBCx33yytII%3DlbmlhidFPvtA7EMVNEsbA2X8sDlDDmWV4J5YhGfBfCAbVbvVkn"
# auth = tweepy.OAuthHandler(api_key, api_secret_key)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, timeout=1200, parser=tweepy.parsers.JSONParser(), wait_on_rate_limit=True, retry_count=3)

def getTweets():
    # using beautiful soup to get data from the Top Grossing Movies of 2019
    base_url = 'https://api.twitter.com/1.1/search/tweets.json?q=from%3Aelonmusk%20%23bitcoin&result_type=popular'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup)
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

# def setUpCategoriesTable(data, cur, conn):
#     category_list = []
#     for business in data['businesses']:
#         business_categories = business['categories']
#         for category in business_categories:
#             if category['title'] not in category_list:
#                 category_list.append(category['title'])

#     cur.execute("DROP TABLE IF EXISTS Categories")
#     cur.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, title TEXT)")
#     for i in range(len(category_list)):
#         cur.execute("INSERT INTO Categories (id,title) VALUES (?,?)",(i,category_list[i]))
#     conn.commit()


def main():
    """Takes nothing as an input and returns nothing. 
    Calls the functions created_tables(), set_up_genre_id_table(), set_up_date_id_table(), 
    set_up_distributor_id_table(), fillup_table(), and write_data_to_file(). Closes the database connection."""
    getTweets()
    # cur, conn = setUpDatabase('movies.db')
    # created_tables(cur, conn)
    # set_up_genre_id_table(cur, conn)
    # set_up_date_id_table(cur, conn)
    # set_up_distributor_id_table(cur,conn)
    # fillup_table(cur, conn)
    # write_data_to_file("movie_data.txt", cur, conn)
    # conn.close()

if __name__ == "__main__":
    main()