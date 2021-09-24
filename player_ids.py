import os
import datetime
import requests
import json
import pandas as pd


class Players:
    """
    A Players object contains functionality to create a dataframe of
    player names and their IDs. The dataframe is stored in a shared file in a
    different directory.
    """

    def update_id_map(self):
        """
        Params: none
        Returns: none
        Check if a dataframe already exists. Update it if it's been more than
        14 days since last update. 
        """
        file_exists = os.path.exists('scraped_info/player_id_dataframe.pkl')
        if file_exists:
            # Check when the df was last updated
            last_updated_epoch = os.path.getmtime('scraped_info/player_id_dataframe.pkl')
            last_updated_date = datetime.date.fromtimestamp(last_updated_epoch)
            cur_date = datetime.date.today()
            time_since_update = cur_date - last_updated_date
            if time_since_update.days > 14:
                self.populate_id_map()
        else:
            self.populate_id_map()
    
    # Create dataframe with one column as player, one column as ID
    def populate_id_map(self):
        """
        Params: none
        Returns: none
        Create a dataframe where one column is all the current NHL players'
        names and the other column is his corresponding ID. 
        """
        id_map = {}
        team_ids = self.get_team_ids()
        for id in team_ids:
            url = 'https://statsapi.web.nhl.com/api/v1/teams/{}?expand=team.roster'.format(id)
            response = requests.get(url).json()
            roster = response['teams'][0]['roster']['roster']
            for player in roster:
                name = player['person']['fullName']
                id = player['person']['id']
                id_map[name] = id
        df = pd.DataFrame(id_map.items(), columns=['Name', 'ID'])
        df.to_pickle('scraped_info/player_id_dataframe.pkl')

    def get_team_ids(self):
        """
        Params: none
        Returns: list of team IDs
        """
        ids = []
        response = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()
        teams = response['teams']
        for team in teams:
            ids.append(team['id'])
        return ids
