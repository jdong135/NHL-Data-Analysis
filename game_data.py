"""
This module fetches live game data
"""

import os
import datetime
import requests
import json
import pandas as pd

def update_game_data():
    """
    Params: none
    Returns: none
    Check if a dataframe already exists. Update it if it's been more than
    14 days since last update. 
    """
    file_exists = os.path.exists('scraped_info/game_data_dataframe.pkl')
    if file_exists:
        # Check when the df was last updated
        last_updated_epoch = os.path.getmtime('scraped_info/game_data_dataframe.pkl')
        last_updated_date = datetime.date.fromtimestamp(last_updated_epoch)
        cur_date = datetime.date.today()
        time_since_update = cur_date - last_updated_date
        if time_since_update.days > 14:
            print('It has been more than 14 days since game_data has been updated')
            get_year_game_data()
    else:
        get_year_game_data()

def get_non_playoff_game_data(season, game_type):
    """
    Params: (int) season, (str) game_type
        Season: ex. 2017 for the 2017-2018 season
        Game types: 01 = preseason, 02 = regular season, 03 = playoffs, 04 = all-star
    Returns: none
    Puts one years game data into pickle, will take a while to run
    """
    game_num = 1
    game_data = []
    # Continue iterating until we go past max games
    while True:
    # for i in range(0, 5):
        ID = str(season) + game_type + str(game_num).zfill(4)
        url = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(ID)
        response = requests.get(url).json()
        if 'messageNumber' in response:
            break
        scoring_plays = response['liveData']['plays']['scoringPlays']
        for p in scoring_plays:
            periodType = response['liveData']['plays']['allPlays'][p]['about']['periodType']
            if periodType == 'OVERTIME' or periodType == 'REGULAR': # Don't care about shootouts
                try:
                    x = response['liveData']['plays']['allPlays'][p]['coordinates']['x']
                    y = response['liveData']['plays']['allPlays'][p]['coordinates']['y']
                except KeyError as e:
                    print(f"No coordinate data for game {game_num}, play {p}")
                name = response['liveData']['plays']['allPlays'][p]['players'][0]['player']['fullName']
                entry = [str(name), abs(int(x)), abs(int(y))]
                game_data.append(entry)
        game_num += 1
    if len(game_data) == 0:
        return
    df = pd.DataFrame(game_data, columns = ['Name', 'Goal_X', 'Goal_Y'])
    return df

def get_playoff_game_data(season):
    """
    """

# df = get_non_playoff_game_data(2017, '02')
# print(df.loc[2])