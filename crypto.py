# Crypto File
from requests import Request, Session
import json
import os
import os.path
import sqlite3
import itertools

TEMP_FILENAME = "run_number.txt"

API_KEY = "8f88d41f-55db-4622-858d-6a7fa5b57d4e"

def get_crypto_data(num):
    ''' Reads in data from CoinMarketCap API and returns dictionary of data including the id, symbol, name, 
        price, percent change in price over 24 hours, and percent change in price over 7 days. 
        Takes in the start number as a parameter (from read_file()), which changes by 25 each time the file is ran'''
    
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start':num+1,
        'limit':'25',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    
    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data

def setUpDatabase(db_name):
    '''takes in database name (crypto.db) as parameter and returns the connection and curser for the database'''
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_crypto_table(data_dict, cur, conn, num):
    ''' takes in the dictionary returned from get_crypto_data() and the connection and the curser from the database as parameters. 
    Creates lists for the crypto id, crypto name, crypto price, percent change over 24 hours, and percent change over 7 days.
    Creates a table for the cryptocurrency data and ensures that only 25 entries are added at a time'''
    
    id_list = []
    name_list = []
    price_list = []
    percent_change_24h_list = []
    percent_change_7d_list = []
    count = 0
    
    for crypto in data_dict['data']:
        id_list.append(crypto['id'])
        name_list.append(crypto['name'])
        price_list.append(crypto['quote']['USD']['price'])
        percent_change_24h_list.append(crypto['quote']['USD']['percent_change_24h'])
        percent_change_7d_list.append(crypto['quote']['USD']['percent_change_7d'])
    
    cur.execute("CREATE TABLE IF NOT EXISTS Crypto (id INTEGER PRIMARY KEY, name TEXT, crypto_id INTEGER, price REAL, percent_change_24h REAL, percent_change_7d REAL)")
    
    # ensure the table stops filling after 25 entried
    count = 0
    for i in range(len(id_list)):
        if count == 25:
            break
        cur.execute("INSERT INTO Crypto (id, name, crypto_id, price, percent_change_24h, percent_change_7d) VALUES (?, ?, ?, ?, ?, ?)", (i+num, name_list[i], id_list[i], price_list[i], percent_change_24h_list[i], percent_change_7d_list[i]))
        if cur.rowcount == 1:
            count += 1

    conn.commit()

def read_file():
    ''' Reads from the run_number file which stores the start number that we will input in get_crypto_data().
        If no file exists (we haven't ran crypto.py yet) then the start number is 0'''
    
    if not os.path.isfile(TEMP_FILENAME):
        return 0
    else:
        f = open(TEMP_FILENAME, "r")
        lines = f.read()
        run_number = int(lines)
        f.close()
        return run_number

def write_file(num):
    ''' Takes num from read_file() as a parameter and writes it to the run_number file'''
    
    f = open(TEMP_FILENAME, "w")
    f.write(str(num))
    f.close()

def main():
    num = read_file()
    data_dict = get_crypto_data(num)
    cur, conn = setUpDatabase('crypto.db')
    write_file(num+25)
    
    make_crypto_table(data_dict, cur, conn, num)

    conn.close()
    


if __name__ == "__main__":
    main()

