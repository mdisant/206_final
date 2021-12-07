import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    return cur, conn

# Create a scatter plot vizualization using matplotlib with the data returned from most_pop_movie
# def viz_one(xlist, ylist):
#     plt.scatter(xlist, ylist, color = "orange")
#     plt.xticks(xlist, rotation = 20)
#     plt.Axes.set_xscale(100, "linear")
#     plt.xlabel("Tweet Count")
#     plt.ylabel("Percentage Increase over 24 Hours")
#     plt.title("Percentage of Price Increase for Cryptocurrency vs Number of Times the Cryptocurrency was Mentioned on Twitter")
#     plt.show()
def viz_one(xlist, ylist):
    fig, ax = plt.subplots()
    ax.scatter(xlist, ylist, color = "orange")
    ax.set_xticks(np.arange(0, 11000, 500))
    plt.xlabel("Tweet Count")
    plt.ylabel("Percentage Increase over 24 Hours")
    plt.title("Percentage of Price Increase for Cryptocurrency over 24 Hours vs Number of Times the Cryptocurrency was Mentioned on Twitter")
    plt.show()
    #discuss outliers


# Create a pie chart vizualization using matplotlib with the data returned from most_pop_movie
def viz_two(xlist, ylist):
    fig, ax = plt.subplots()
    ax.scatter(xlist, ylist, color = "blue")
    ax.set_xticks(np.arange(0, 11000, 500))
    plt.xlabel("Tweet Count")
    plt.ylabel("Percentage Increase over 7 days")
    plt.title("Percentage of Price Increase for Cryptocurrency over 7 Days vs Number of Times the Cryptocurrency was Mentioned on Twitter")
    plt.show()

# Uncomment this to make sure your function works
# uncomment these one at a time to see the visualizations
def main():

    cur,conn = setUpDatabase('crypto.db') #make fucntion 
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
