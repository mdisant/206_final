import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    return cur, conn


def viz_one(xlist, ylist):
    fig, ax = plt.subplots()
    ax.scatter(xlist, ylist, color = "orange")
    ax.set_xticks(np.arange(0, 12000, 500))
    ax.set_xlim(0, 5000) # gets rid of outliers 
    plt.xlabel("Tweet Count")
    plt.ylabel("Percentage Increase over 24 Hours")
    plt.title("Percentage of Price Increase for Cryptocurrency over 24 Hours vs Number of Times the Cryptocurrency was Mentioned on Twitter")
    plt.show()
    #discuss outliers


# Create a scatter chart vizualization using matplotlib with the data returned from Combined table
def viz_two(xlist, ylist):
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
    # select statement 
    cur.execute("SELECT count FROM Combined")
    count_list = cur.fetchall()
    cur.execute("SELECT increase_24h FROM Combined")
    hour_list = cur.fetchall()
    viz_one(count_list, hour_list)
    cur.execute("SELECT increase_7d FROM Combined")
    day_list = cur.fetchall()
    viz_two(count_list, day_list)

    conn.close()

if __name__ == "__main__":
    main()
