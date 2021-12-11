import matplotlib.pyplot as plt
# Credit to https://towardsdatascience.com/nhl-analytics-with-python-6390c5d3206d
# for help with creating canvas


fig = plt.figure(figsize=(10, 10))
rink = fig.add_subplot(111)
rink.set_facecolor('white') # Sets inside of plot to white
fig.patch.set_facecolor('white') # Sets outside of plot to white
rink.set_xticks([])
rink.set_yticks([])
photo=plt.imread("half_rink.jpeg")
rink.imshow(photo)
plt.show()
