"""
Player object:
Contains career stats and methods to graph these stats
"""

import player_ids
import requests
import matplotlib.pyplot as plt
import api
import canvas

class Player:
    def __init__(self, name):
        self.name = name
        self.id = player_ids.get_player_id(name)
        if self.id == -1:
            raise ValueError(f'{name} not found in database')
        # {20052006: {assists, goals, pim, games, penalty minutes, plusMinus, points}}
        self.career_stats = {}
        # Abbreviate seasons: 2010-2011 -> '10-'11
        self.seasons = []
    
    def populate_career_stats(self):
        """
        Params: none
        Returns: none
        Populates player's stats in a dictionary in the form of
            {season number: {dictionary of stats}}.
        Populates player's seasons in NHL as list ['10-'11, '11-'12, ...].
        This method only considers NHL stats. If a player played for multiple
        teams during a season, it accumulates the totals across teams.
        """
        self.career_stats = api.get_career_statistics(self.id)
        self.seasons = api.get_career_seasons(self.id)

    def get_career_goals(self):
        """
        Params: none
        Returns: (list) goals for each season
        """
        if not self.seasons:
            self.populate_career_stats()
        career_goals = []
        for season in self.career_stats.keys():
            goals = self.career_stats[season]['goals']
            career_goals.append(goals)
        return career_goals

    def graph_career_goals(self):
        """
        Params: none
        Returns: none
        Plots season vs. goals scored
        """
        career_goals = self.get_career_goals()
        canvas.line_graph(self.seasons, career_goals, 'Season vs. Goals', 'Season', 'Goals Scored')

    def get_stat_names(self):
        """
        Params: none
        Returns: (list) of stat names measured for this player
        Uses the first season the player was in, in case more metrics are
        tracked in later seasons
        """
        if not self.seasons:
            self.populate_career_stats()
        first_season = list(self.career_stats.keys())[0]
        first_season_stats = self.career_stats[first_season]
        return list(first_season_stats.keys())
    
    # Add in functionality for playoff data
    def draw_goals(self, season, season_type):
        """
        Params: (int) season, (string) season type
        Returns: none
        Plots player's goals in given season
        """
        df = api.get_non_playoff_goal_coords(season, season_type)
        player_df = df[df.iloc[:,0] == self.name]
        canvas.draw_points(player_df.iloc[:,1].values.tolist(), player_df.iloc[:,2].values.tolist())


# TODO:
# Refactor Player class
# Add in playoff data compatibility