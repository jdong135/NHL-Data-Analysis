"""
This module contains functions related to setting and getting player IDs. 
"""

import os
import datetime
import requests
import json
import pandas as pd


def update_id_map():
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
            populate_id_map()
    else:
        populate_id_map()

def populate_id_map(self):
    """
    Params: none
    Returns: none
    Create a dataframe where one column is all the current NHL players'
    names and the other column is his corresponding ID. 
    """
    id_map = {}
    team_ids = get_team_ids()
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

# CONSIDER ABSTRACTING
def get_team_ids():
    """
    Params: none
    Returns: (list) of team IDs
    """
    ids = []
    response = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()
    teams = response['teams']
    for team in teams:
        ids.append(team['id'])
    return ids

def get_player_id(name):
    """
    Input: (str) name of player
    Returns: (int) ID of inputted player
    If player is not found in dataframe, return -1
    """
    df = pd.read_pickle('scraped_info/player_id_dataframe.pkl')
    id = df['ID'].where(df['Name'] == name)
    id = id.dropna()
    if id.empty:
        return -1
    else:
        # If there are duplicate names, fetch the first one
        return int(id.iloc[0])
