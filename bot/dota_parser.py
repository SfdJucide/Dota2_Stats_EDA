import requests


def get_heroes():
    url = "https://api.opendota.com/api/heroStats"
    response = requests.get(url)
    if response.status_code == 200:

        return response.json()
    
def get_items():
    url="https://api.opendota.com/api/constants/item_ids"
    response = requests.get(url)
    if response.status_code == 200:

        return response.json().items()
    
def get_regions():
    url="https://api.opendota.com/api/constants/region"
    response = requests.get(url)
    if response.status_code == 200:

        return response.json().items()
    
def get_lobby_types():
    url="https://api.opendota.com/api/constants/lobby_type"
    response = requests.get(url)
    if response.status_code == 200:

        return response.json().values()
    
def get_game_modes():
    url="https://api.opendota.com/api/constants/game_mode"
    response = requests.get(url)
    if response.status_code == 200:

        return response.json().values()

def get_matches_ids():
    url = "https://api.opendota.com/api/publicMatches"
    response = requests.get(url)
    ids_list = []
    if response.status_code == 200:
        for game in response.json():
            ids_list.append(game['match_id'])

        return ids_list
    
def get_matches(ids_list):
    matches = []

    for match_id in ids_list:
        url = f"https://api.opendota.com/api/matches/{match_id}"
        response = requests.get(url)
        if response.status_code == 200:
            matches.append(response.json())

    return matches

def get_matches_info(matches):
    parsed_matches = []

    for game in matches:
        game_info = {
            "match_id": game['match_id'],
            "duration": game['duration'],
            "first_blood_time": game['first_blood_time'],
            "game_mode": game['game_mode'],
            "human_players": game['human_players'],
            "lobby_type": game['lobby_type'],
            "start_time": game['start_time'],
            "region": game['region'],
            "players": game['players'],
            "dire_score": game['dire_score'],
            "radiant_score": game['radiant_score'],
            "radiant_win": game['radiant_win'],
        }
        parsed_matches.append(game_info)

    return parsed_matches
