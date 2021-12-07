import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
from statistics import stdev

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

def calculate_correlation(xlist_tups, ylist_tups):
    xlist = [tup[0] for tup in xlist_tups]
    ylist = [tup[0] for tup in ylist_tups]

    r = 0
    
    stdev_x = stdev(xlist)
    stdev_y = stdev(ylist)
    avg_x = sum(xlist) / len(xlist)
    avg_y = sum(ylist) / len(ylist)

    for i in range(len(xlist)):
        x_dif = (xlist[i] - avg_x) / stdev_x
        y_dif = (ylist[i] - avg_y) / stdev_y
        r += x_dif * y_dif
    
    corr = r * r
    return corr

def main():

    cur,conn = setUpDatabase('crypto.db') 
    # select statement 
    cur.execute("SELECT count FROM Combined")
    count_list = cur.fetchall()
    cur.execute("SELECT increase_24h FROM Combined")
    hour_list = cur.fetchall()
    viz_one(count_list, hour_list)
    calculate_correlation(count_list, hour_list)
    cur.execute("SELECT increase_7d FROM Combined")
    day_list = cur.fetchall()
    viz_two(count_list, day_list)

    conn.close()

if __name__ == "__main__":
    main()
