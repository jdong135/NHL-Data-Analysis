"""
Player object:
Contains career stats and methods to graph these stats
"""

import player_ids
import requests
import matplotlib.pyplot as plt

class Player:
    def __init__(self, name):
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
        This method only considers NHL stats. If a player played for multiple
        teams during a season, it accumulates the totals across teams.
        """
        url = f'https://statsapi.web.nhl.com/api/v1/people/{self.id}/stats?stats=yearByYear'
        response = requests.get(url).json()
        season_stats = response['stats'][0]['splits']
        for stat in season_stats:
            if stat['league']['name'] == 'National Hockey League':
                season = stat['season']
                # There may be repeat seasons because players get traded,
                # accumulate statistics if so
                if season in self.career_stats.keys():
                    for key, value in stat['stat'].items():
                        # Handle adding times together
                        if ':' in str(value):
                            cur_time = self.career_stats[season][key].split(':')
                            cur_seconds = int(cur_time[1])
                            cur_mins = int(cur_time[0])
                            delta_time = value.split(':')
                            delta_seconds = int(delta_time[1])
                            delta_mins = int(delta_time[0])
                            new_seconds = cur_seconds + delta_seconds
                            if new_seconds >= 60:
                                new_minutes = cur_mins + delta_mins + 1
                                new_seconds -= 60
                            else:
                                new_minutes = cur_mins + delta_mins
                            self.career_stats[season][key] = f'{str(new_minutes)}:{str(new_seconds)}'
                        else:
                            self.career_stats[season][key] += value
                else:
                    stats = stat['stat']
                    self.career_stats[season] = stats
                    season_abbrev = f'\'{season[2:4]}-\'{season[-2:]}'
                    if season_abbrev not in self.seasons:
                        self.seasons.append(season_abbrev)

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
        Plots goals scored vs. season
        """
        career_goals = self.get_career_goals()
        plt.figure(figsize=(10, 6))
        plt.plot(self.seasons, career_goals, marker='o')
        plt.title('Season vs. Goals')
        plt.xlabel('Season')
        plt.ylabel('Goals Scored')
        plt.show()

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