import os
import datetime
import requests
import json
import pandas as pd

# Map of {player: id number}
class Players:
    def __init__(self):
        self.id_map = {}

    def get_id_map(self):
        # If scraped_info dataframe doesn't exist, run scrape
        file_exists = os.path.exists('scraped_info/player_id_dataframe.pkl')
        if file_exists:
            # Check when the df was last updated
            last_updated_epoch = os.path.getmtime('scraped_info/player_id_dataframe.pkl')
            last_updated_date = datetime.datetime.fromtimestamp(last_updated_epoch)
            cur_date = datetime.date.today()
            time_since_update = cur_date - last_updated_date
            if time_since_update.days > 14:
                # Scrape again
                self.scrape()
            else:
                # Return existing dataframe
                return
        else:
            self.scrape()
    # Create dataframe with one column as player, one column as ID
    def scrape(self):
        team_ids = self.get_team_ids()
        for id in team_ids:
            url = 'https://statsapi.web.nhl.com/api/v1/teams/{}?expand=team.roster'.format(id)
            response = requests.get(url).json()
            roster = response['teams'][0]['roster']['roster']
            for player in roster:
                name = player['person']['fullName']
                id = player['person']['id']
                self.id_map[name] = id
        df = pd.DataFrame(self.id_map.items(), columns=['Name', 'ID'])
        df.to_pickle('scraped_info/player_id_dataframe.pkl')
        return self.id_map

    def get_team_ids(self):
        ids = []
        response = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()
        teams = response['teams']
        for team in teams:
            ids.append(team['id'])
        return ids
