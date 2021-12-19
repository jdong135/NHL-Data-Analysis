"""
This module handles making requests to the API
"""

import os
import datetime
import requests
import json
import pandas as pd

def get_career_seasons(player_id):
    """
    Params: (int) player ID
    Returns: (list) abbreviated version of player seasons; 2010-2011 -> '10-'11
    """
    url = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=yearByYear'
    response = requests.get(url).json()
    season_stats = response['stats'][0]['splits']
    seasons = []
    for stat in season_stats:
        if stat['league']['name'] == 'National Hockey League':
            season = stat['season']
            season_abbrev = f'\'{season[2:4]}-\'{season[-2:]}'
            if season_abbrev not in seasons:
                seasons.append(season_abbrev)
    return seasons

def get_career_statistics(player_id):
    """
    Params: (int) player ID
    Returns: (dict) ex. {20052006: {assists, goals, pim, games, penalty minutes, plusMinus, points}}
    """
    url = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=yearByYear'
    response = requests.get(url).json()
    season_stats = response['stats'][0]['splits']
    career_stats = {}
    for stat in season_stats:
        if stat['league']['name'] == 'National Hockey League':
            season = stat['season']
            # There may be repeat seasons because players get traded,
            # accumulate statistics if so
            if season in career_stats.keys():
                for key, value in stat['stat'].items():
                    # Handle adding times together
                    if ':' in str(value):
                        cur_time = career_stats[season][key].split(':')
                        cur_seconds, cur_mins = int(cur_time[1]), int(cur_time[0])
                        delta_time = value.split(':')
                        delta_seconds, delta_mins = int(delta_time[1]), int(delta_time[0])
                        new_seconds = cur_seconds + delta_seconds
                        if new_seconds >= 60:
                            new_minutes = cur_mins + delta_mins + 1
                            new_seconds -= 60
                        else:
                            new_minutes = cur_mins + delta_mins
                        career_stats[season][key] = f'{str(new_minutes)}:{str(new_seconds)}'
                    else:
                        career_stats[season][key] += value
            else:
                stats = stat['stat']
                career_stats[season] = stats
    return career_stats

def get_non_playoff_goal_coords(season, game_type):
    """
    Params: (int) season, (str) game_type
        Season: ex. 2017 for the 2017-2018 season
        Game types: 01 = preseason, 02 = regular season, 03 = playoffs, 04 = all-star
    Returns: dataframe of player names, and coordinate of goals scored
    This method takes a long time to run
    """
    game_num = 1
    game_data = []
    # Continue iterating until we go past max games
    while True:
    # for i in range(1, 100):
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
