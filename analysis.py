# Hexbin inspiration: https://towardsdatascience.com/nhl-analytics-with-python-6390c5d3206d

import player_ids
import player
import matplotlib.pyplot as plt

player_ids.update_id_map()
kane = player.Player("Patrick Kane")
kane.draw_goals(2018, '02')



# def draw_goal_distribution():
#     df = game_data.get_non_playoff_game_data(2018, '02')
#     # pkane = df[df.iloc[:,0] == 'Patrick Kane']
#     x = df.iloc[:,1]
#     y = df.iloc[:,2]
#     hex_bin = plt.hexbin(x, y, gridsize=20, mincnt=1, extent=[-100, 100, -100, 100])
#     centers = hex_bin.get_offsets()
#     frequencies = hex_bin.get_array()
#     canvas.draw_points()
#     plt.show()