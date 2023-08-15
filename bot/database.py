import sqlite3


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('dota_2.db')
        self.cursor = self.connection.cursor()

    def create_matches_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Matches (
                        match_id INT PRIMARY KEY,
                        duration INT,
                        first_blood_time INT, 
                        game_mode INT, 
                        human_players INT, 
                        lobby_type INT, 
                        start_time INT, 
                        region INT, 
                        dire_score INT, 
                        radiant_score INT, 
                        radiant_win INT
                    );
                    """
            self.cursor.execute(query)
    
    def create_players_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Players (
                        record_id INT PRIMARY KEY,
                        match_id INT,
                        assists INT,
                        deaths INT, 
                        denies INT,
                        gold INT, 
                        gold_per_min INT, 
                        gold_spent INT, 
                        hero_damage INT, 
                        hero_healing INT, 
                        hero_id INT,
                        item_0 INT,
                        item_1 INT,
                        item_2 INT,
                        item_3 INT,
                        item_4 INT,
                        item_5 INT,
                        item_neutral INT,
                        kills INT,
                        last_hits INT,
                        level INT,
                        net_worth INT,
                        tower_damage INT,
                        xp_per_min INT,
                        isRadiant INT
                    );
                    """
            self.cursor.execute(query)

    def create_heroes_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Heroes (
                        hero_id INT PRIMARY KEY,
                        name TEXT,
                        primary_attr TEXT, 
                        attack_type TEXT, 
                        base_health INT, 
                        base_health_regen REAL, 
                        base_mana INT, 
                        base_mana_regen REAL, 
                        base_armor INT, 
                        base_mr INT, 
                        base_attack_min INT,
                        base_attack_max INT, 
                        base_str INT, 
                        base_agi INT,
                        base_int INT,
                        str_gain REAL,
                        agi_gain REAL,
                        int_gain REAL,
                        attack_range INT,
                        projectile_speed INT,
                        attack_rate REAL,
                        base_attack_time INT,
                        attack_point REAL,
                        move_speed INT,
                        legs INT,
                        day_vision INT,
                        night_vision INT
                    );
                    """
            self.cursor.execute(query)
    
    def create_items_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Items (
                        item_id INT PRIMARY KEY,
                        name TEXT
                    );
                    """
            self.cursor.execute(query)

    def create_regions_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Regions (
                        region_id INT PRIMARY KEY,
                        name TEXT
                    );
                    """
            self.cursor.execute(query)

    def create_game_modes_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Game_modes (
                        gm_id INT PRIMARY KEY,
                        name TEXT
                    );
                    """
            self.cursor.execute(query)
    
    def create_lobby_types_table(self) -> None:
        with self.connection:
            query = """
                    CREATE TABLE IF NOT EXISTS Lobby_types (
                        lt_id INT PRIMARY KEY,
                        name TEXT
                    );
                    """
            self.cursor.execute(query)

    def create_heroes_index(self) -> None:
        with self.connection:
            query = """
                    CREATE INDEX IF NOT EXISTS idx_name
                    ON Heroes (name);
                    """

            self.cursor.execute(query)

    def insert_matches(self, matches) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Matches
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            for game in matches:
                self.cursor.execute(query, (
                                    game['match_id'],
                                    game['duration'],
                                    game['first_blood_time'],
                                    game['game_mode'],
                                    game['human_players'],
                                    game['lobby_type'],
                                    game['start_time'],
                                    game['region'],
                                    game['dire_score'],
                                    game['radiant_score'],
                                    game['radiant_win'],)
                                    )
                self.insert_players(game['players'])

    def insert_players(self, players) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Players
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            for player in players:
                self.cursor.execute(query, (
                                    int(str(player['match_id']) + str(player['hero_id'])),
                                    player['match_id'],
                                    player['assists'],
                                    player['deaths'],
                                    player['denies'],
                                    player['gold'],
                                    player['gold_per_min'],
                                    player['gold_spent'],
                                    player['hero_damage'],
                                    player['hero_healing'],
                                    player['hero_id'],
                                    player['item_0'],
                                    player['item_1'],
                                    player['item_2'],
                                    player['item_3'],
                                    player['item_4'],
                                    player['item_5'],
                                    player['item_neutral'],
                                    player['kills'],
                                    player['last_hits'],
                                    player['level'],
                                    player['net_worth'],
                                    player['tower_damage'],
                                    player['xp_per_min'],
                                    player['isRadiant'],)
                                    )
    def insert_heroes(self, heroes) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Heroes
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            for hero in heroes:
                self.cursor.execute(query, (
                                    hero['id'],
                                    hero['localized_name'],
                                    hero['primary_attr'],
                                    hero['attack_type'],
                                    hero['base_health'],
                                    hero['base_health_regen'],
                                    hero['base_mana'],
                                    hero['base_mana_regen'],
                                    hero['base_armor'],
                                    hero['base_mr'],
                                    hero['base_attack_min'],
                                    hero['base_attack_max'],
                                    hero['base_str'],
                                    hero['base_agi'],
                                    hero['base_int'],
                                    hero['str_gain'],
                                    hero['agi_gain'],
                                    hero['int_gain'],
                                    hero['attack_range'],
                                    hero['projectile_speed'],
                                    hero['attack_rate'],
                                    hero['base_attack_time'],
                                    hero['attack_point'],
                                    hero['move_speed'],
                                    hero['legs'],
                                    hero['day_vision'],
                                    hero['night_vision'],)
                                    )
                
    def insert_items(self, items) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Items
                    VALUES (?, ?)
                    """
            for item in items:
                self.cursor.execute(query, (int(item[0]), item[1]))

    def insert_regions(self, regions) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Regions
                    VALUES (?, ?)
                    """
            for region in regions:
                self.cursor.execute(query, (int(region[0]), region[1]))

    def insert_game_modes(self, game_mods) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Game_modes
                    VALUES (?, ?)
                    """
            for gm in game_mods:
                self.cursor.execute(query, (gm['id'], gm['name']))

    def insert_lobby_types(self, lobby_types) -> None:
        with self.connection:
            query = """
                    INSERT OR IGNORE INTO Lobby_types
                    VALUES (?, ?)
                    """
            for lt in lobby_types:
                self.cursor.execute(query, (lt['id'], lt['name']))
    
    def get_matches_number(self) -> int:
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM Matches").fetchone()[0]
        
    def get_avg_game_duration(self) -> float:
        with self.connection:
            return self.cursor.execute("SELECT ROUND(AVG(duration), 2) FROM Matches").fetchone()[0]
        
    def get_avg_fb_timing(self) -> float:
        with self.connection:
            return self.cursor.execute("SELECT ROUND(AVG(first_blood_time), 2) FROM Matches").fetchone()[0]
        
    def get_avg_team_score(self, team: str) -> float:
        with self.connection:
            if team == 'dire':
                score = self.cursor.execute("SELECT ROUND(AVG(dire_score), 2) FROM Matches").fetchone()[0]
            elif team == 'radiant':
                score = self.cursor.execute("SELECT ROUND(AVG(radiant_score), 2) FROM Matches").fetchone()[0]
            
            return score
        
    def get_team_winrate(self, team: str) -> float:
        with self.connection:
            if team == 'dire':
                winrate = self.cursor.execute("SELECT 100 - ROUND(AVG(radiant_win) * 100, 2) FROM Matches").fetchone()[0]
            elif team == 'radiant':
                winrate = self.cursor.execute("SELECT ROUND(AVG(radiant_win) * 100, 2) FROM Matches").fetchone()[0]
            
            return winrate
        
    def get_heroes_names_by_attr(self, attr: str):
        with self.connection:
            return self.cursor.execute(f"SELECT hero_id, name FROM Heroes WHERE primary_attr == '{attr}'").fetchall()
        
    def get_hero_statistic(self, hero_id: int):
        with self.connection:
            games_number = self.cursor.execute("SELECT COUNT(*) FROM Matches WHERE duration > 60*10").fetchone()[0]
            query = f"""
                    SELECT 
                        name,
                        COUNT(m.match_id) as total_games,
                        ROUND(COUNT(record_id) * 1.0 / {games_number} * 100, 2) as pick_rate,
                        ROUND(SUM(CASE WHEN isRadiant = radiant_win THEN 1 ELSE 0 END) * 1.0 / COUNT(m.match_id) * 100, 2) as win_rate,
                        ROUND(AVG(kills), 2) as kills,
                        ROUND(AVG(deaths), 2) as deaths,
                        ROUND(AVG(assists), 2) as assists,
                        ROUND(AVG(last_hits), 2) as last_hits,
                        ROUND(AVG(denies), 2) as denies,
                        ROUND(AVG(hero_damage), 2) as hero_damage,
                        ROUND(AVG(hero_healing), 2) as hero_healing,
                        ROUND(AVG(net_worth), 2) as net_worth,
                        ROUND(AVG(tower_damage), 2) as tower_damage,
                        ROUND(AVG(gold_per_min), 2) as gold_per_min,
                        ROUND(AVG(xp_per_min), 2) as xp_per_min,
                        ROUND(AVG(duration), 2) as average_game_duration
                    FROM Players as p
                    JOIN Heroes as h 
                    ON h.hero_id == p.hero_id
                    JOIN Matches as m
                    ON p.match_id == m.match_id
                    WHERE p.hero_id == {hero_id} and duration > 60*10
                    """
            return self.cursor.execute(query).fetchone()

