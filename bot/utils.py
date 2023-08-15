from database import Database
import dota_parser as dp
import time

db = Database()

def get_hero_stats(hero_id: int) -> str:
    hero_stats = db.get_hero_statistic(hero_id)
    duration = f'{int(hero_stats[15] // 60):02}:{int(hero_stats[15] % 60):02}'
    hero_str = f'Name: {hero_stats[0]}\nTotal games: {hero_stats[1]}\nPick Rate: {hero_stats[2]}%\nWin Rate: {hero_stats[3]}%\nKills: {hero_stats[4]}\nDeaths: {hero_stats[5]}\nAssists: {hero_stats[6]}\nLast hits: {hero_stats[7]}\nDenies: {hero_stats[8]}\nHero damage: {hero_stats[9]}\nHero healing: {hero_stats[10]}\nNet worth: {hero_stats[11]}\nTower damage: {hero_stats[12]}\nGPM: {hero_stats[13]}\nXPM: {hero_stats[14]}\nAverage game duration: {duration}'
    return hero_str

def get_heroes_names(attr: str):
    return db.get_heroes_names_by_attr(attr)

def get_avg_scores() -> str:
    dire_score = db.get_avg_team_score('dire')
    radiant_score = db.get_avg_team_score('radiant')
    return f'Radiant score {radiant_score} VS Dire score {dire_score}'

def get_teams_winrates() -> str:
    dire_wr = db.get_team_winrate('dire')
    radiant_wr = db.get_team_winrate('radiant')
    return f'Radiant {radiant_wr}% VS Dire {dire_wr}%'

def get_avg_duration() -> str:
    avg_dur = db.get_avg_game_duration()
    return f'{int(avg_dur // 60):02}:{int(avg_dur % 60):02}'

def get_avg_first_blood() -> str:
    avg_time = db.get_avg_fb_timing()
    return f'{int(avg_time // 60):02}:{int(avg_time % 60):02}'

def create_tables() -> None:
    db.create_heroes_table()
    db.create_items_table()
    db.create_regions_table()
    db.create_game_modes_table()
    db.create_lobby_types_table()
    db.create_players_table()
    db.create_matches_table()
    db.create_heroes_index()

def insert_static_data() -> None:
    hero_list = dp.get_heroes()
    items_list = dp.get_items()
    region_list = dp.get_regions()
    gm_list = dp.get_game_modes()
    lt_list = dp.get_lobby_types()

    db.insert_heroes(heroes=hero_list)
    db.insert_items(items=items_list)
    db.insert_regions(regions=region_list)
    db.insert_game_modes(game_mods=gm_list)
    db.insert_lobby_types(lobby_types=lt_list)

def parse_matches(times: int=20) -> None:
    for i in range(times):
        try:
            matches_list = dp.get_matches_info(dp.get_matches(dp.get_matches_ids()))
            db.insert_matches(matches=matches_list)
            time.sleep(60)
        except TypeError:
            pass
