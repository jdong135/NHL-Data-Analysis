import matplotlib.pyplot as plt
import pandas as pd
# Credit to https://towardsdatascience.com/nhl-analytics-with-python-6390c5d3206d
# for help with creating canvas

# Coordinates of shots taken from API:
# 0 <= Goal_Y <= 42.5
# 0 <= Goal_X <= 100

# White part of rink for scaling:
RINK_X_MIN = 0
RINK_X_MAX = 550
RINK_Y_MIN = 20
RINK_Y_MAX = 560
Y_SCALE = (RINK_Y_MAX - RINK_Y_MIN) / 42.5
X_SCALE = (RINK_X_MAX - RINK_X_MIN) / 100

def draw_rink():
    fig = plt.figure(figsize=(8, 8))
    rink = fig.add_subplot(111)
    rink.set_facecolor('white') # Sets inside of plot to white
    fig.patch.set_facecolor('white') # Sets outside of plot to white
    rink.set_xticks([])
    rink.set_yticks([])
    photo=plt.imread("half_rink.jpeg")
    rink.imshow(photo)
    return rink

def draw_points(x, y):
    """
    Params: (list) x, (list) y of x and y coordinates
    Returns: none

    Plots points on canvas with half rink backdrop
    """
    rink = draw_rink()
    for i in range(len(x)):
        # Need to add 15 to y coordinate to offset the black rink wall
        circle = plt.Circle((x[i] * X_SCALE, y[i] * Y_SCALE + 15), 5, color='black')
        rink.add_patch(circle)
    plt.show()

def line_graph(x, y, title, x_label, y_label):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()