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

def draw_points(points):
    rink = draw_rink()
    for _, row in points.iterrows():
        # Need to add 15 to y coordinate to offset the black rink wall
        circle = plt.Circle((row["Goal_X"] * X_SCALE, row["Goal_Y"] * Y_SCALE + 15), 5, color='b')
        rink.add_patch(circle)
    plt.show()

