# Crypto File
from requests import Request, Session
import json
import os
import sqlite3


API_KEY = "8f88d41f-55db-4622-858d-6a7fa5b57d4e"

def get_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start':'1',
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
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_crypto_table(data_dict, cur, conn):
    id_list = []
    name_list = []
    price_list = []
    percent_change_24h_list = []
    percent_change_7d_list = []
    
    for crypto in data_dict['data']:
        id_list.append(crypto['id'])
        name_list.append(crypto['name'])
        price_list.append(crypto['quote']['USD']['price'])
        percent_change_24h_list.append(crypto['quote']['USD']['percent_change_24h'])
        percent_change_7d_list.append(crypto['quote']['USD']['percent_change_7d'])
    
    cur.execute("DROP TABLE IF EXISTS Crypto")
    cur.execute("CREATE TABLE Crypto (id INTEGER PRIMARY KEY, name TEXT, crypto_id INTEGER, price REAL, percent_change_24h REAL, percent_change_7d REAL)")
    for i in range(len(id_list)):
        cur.execute("INSERT INTO Crypto (id, name, crypto_id, price, percent_change_24h, percent_change_7d) VALUES (?, ?, ?, ?, ?, ?)", (i, name_list[i], id_list[i], price_list[i], percent_change_24h_list[i], percent_change_7d_list[i]))
    conn.commit()

def main():
    data_dict = get_crypto_data()
    cur, conn = setUpDatabase('crypto.db')
    
    make_crypto_table(data_dict, cur, conn)

    conn.close()
    


if __name__ == "__main__":
    main()

