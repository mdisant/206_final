import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np


# Create a scatter plot vizualization using matplotlib with the data returned from most_pop_movie
def viz_one(xlist, ylist):
    plt.scatter(xlist, ylist, color = "orange")
    plt.xticks(name, rotation = 20)
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title("Number of Votes for Movies")
    plt.show()


# Create a pie chart vizualization using matplotlib with the data returned from most_pop_movie
def viz_two(data):
    names = []
    votes = []
    for i in data:
        names.append(i[1])
        votes.append(i[0])
    plt.pie(votes, labels=names)
    #pie(y values, labels)
    plt.show()

# Uncomment this to make sure your function works
# uncomment these one at a time to see the visualizations
viz_one()
viz_two(data)