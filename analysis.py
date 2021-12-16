import player_ids
import player
import canvas
import game_data

# player_ids.update_id_map()
# kane = player.Player("Patrick Kane")
# kane.graph_career_goals()

df = game_data.get_non_playoff_game_data(2018, '02')
# print(df[["Goal_Y"]])
# print(df[ df.iloc[:,2] <= 10 ])
print(df[df.iloc[:,0] == 'Patrick Kane'])
canvas.draw_points(df[df.iloc[:,0] == 'Patrick Kane'])