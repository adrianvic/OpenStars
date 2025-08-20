import pymysql
import datetime
import json
import Config
from Utils.Logger import Logger
from Logic.Player import Player
from DataBase.SQLUtils import SQLUtils

class SQLDatabase:
    def __init__(self):
        self.player = Player
        self.client = pymysql.connect(
            host=Config.config["DBConnectionURL"],
            user=Config.config["SQLUser"],
            password=Config.config["SQLPassword"],
            database=Config.config["SQLDatabase"],
            cursorclass=pymysql.cursors.DictCursor
        )
        Logger.log("debug", f"Connected to MariaDB {Config.config['SQLDatabase']}")
        self.sql_utils = SQLUtils(self.client)

        self.data = {
            'Name': 'Guest',
            'NameSet': False,
            'Gems': Player.gems,
            'Trophies': Player.trophies,
            'Tickets': Player.tickets,
            'Resources': Player.resources,  # list/dict fields
            'TokenDoubler': 0,
            'HighestTrophies': Player.high_trophies,
            'HomeBrawler': 0,
            'TrophyRoadReward': 1,
            'ExperiencePoints': Player.exp_points,
            'ProfileIcon': 0,
            'NameColor': 0,
            'UnlockedBrawlers': Player.brawlers_unlocked,
            'BrawlersTrophies': Player.brawlers_trophies,
            'BrawlersHighestTrophies': Player.brawlers_high_trophies,
            'BrawlersLevel': Player.brawlers_level,
            'BrawlersPowerPoints': Player.brawlers_powerpoints,
            'UnlockedSkins': Player.unlocked_skins,
            'SelectedSkins': Player.selected_skins,
            'SelectedBrawler': 0,
            'Region': Player.region,
            'SupportedContentCreator': "Classic Brawl",
            'StarPower': Player.starpower,
            'Gadget': Player.gadget,
            'BrawlPassActivated': False,
            'WelcomeMessageViewed': False,
            'ClubID': 0,
            'ClubRole': 1,
            'TimeStamp': str(datetime.datetime.now())
        }

        self.club_data = {
            'Name': '',
            'Description': '',
            'Region': '',
            'BadgeID': 0,
            'Type': 0,
            'Trophies': 0,
            'RequiredTrophies': 0,
            'FamilyFriendly': 0,
            'Members': [],  # list
            'Messages': []  # list
        }

    def merge(self, dict1, dict2):
        merged = dict1.copy()
        merged.update(dict2)
        return merged

    # --- Helpers ---
    @staticmethod
    def _serialize_fields(data, fields):
        for key in fields:
            if key in data and isinstance(data[key], (dict, list)):
                data[key] = json.dumps(data[key])
        return data

    @staticmethod
    def _deserialize_fields(data, fields):
        for key in fields:
            if key in data and isinstance(data[key], str):
                try:
                    data[key] = json.loads(data[key])
                except json.JSONDecodeError:
                    pass
        return data

    JSON_PLAYER_FIELDS = ['Resources','UnlockedBrawlers','BrawlersTrophies','BrawlersHighestTrophies',
                          'BrawlersLevel','BrawlersPowerPoints','UnlockedSkins','SelectedSkins']

    JSON_CLUB_FIELDS = ['Members','Messages']

    # --- Player methods ---
    def create_player_account(self, id, token):
        auth = self.merge({'ID': id, 'Token': token}, self.data)
        auth = self._serialize_fields(auth, self.JSON_PLAYER_FIELDS)
        self.sql_utils.insert_data("Players", auth)
    
    def load_player_account(self, id, token):
        query = {"Token": token}
        result = self.sql_utils.load_document("Players", query)
        if result:
            for x in self.data:
                if x not in result:
                    self.update_player_account(token, x, self.data[x])
            result = self.sql_utils.load_document("Players", query)
            result = self._deserialize_fields(result, self.JSON_PLAYER_FIELDS)
        return result

    def load_player_account_by_id(self, id):
        query = {"ID": id}
        result = self.sql_utils.load_document("Players", query)
        if result:
            result = self._deserialize_fields(result, self.JSON_PLAYER_FIELDS)
        return result

    def update_player_account(self, token, item, value):
        if item in self.JSON_PLAYER_FIELDS:
            value = json.dumps(value)
        self.sql_utils.update_document("Players", {"Token": token}, item, value)

    def update_all_players(self, query, item, value):
        if item in self.JSON_PLAYER_FIELDS:
            value = json.dumps(value)
        self.sql_utils.update_all_documents("Players", query, item, value)

    def delete_all_players(self, args):
        self.sql_utils.delete_all_documents("Players", args)

    def delete_player(self, token):
        self.sql_utils.delete_document("Players", {"Token": token})

    def load_all_players(self, args):
        result = self.sql_utils.load_all_documents("Players", args)
        for r in result:
            self._deserialize_fields(r, self.JSON_PLAYER_FIELDS)
        return result

    def load_all_players_sorted(self, args, element, element2=None):
        result = self.sql_utils.load_all_documents_sorted("Players", args, element, element2)
        for r in result:
            self._deserialize_fields(r, self.JSON_PLAYER_FIELDS)
        return result

    # --- Club methods ---
    def create_club(self, id, data):
        auth = self.merge({'ID': id}, data)
        auth = self._serialize_fields(auth, self.JSON_CLUB_FIELDS)
        self.sql_utils.insert_data("Clubs", auth)

    def update_club(self, id, item, value):
        if item in self.JSON_CLUB_FIELDS:
            value = json.dumps(value)
        self.sql_utils.update_document("Clubs", {"ID": id}, item, value)

    def load_club(self, id):
        query = {"ID": id}
        result = self.sql_utils.load_document("Clubs", query)
        if result:
            for x in self.club_data:
                if x not in result:
                    self.update_club(id, x, self.club_data[x])
            result = self.sql_utils.load_document("Clubs", query)
            result = self._deserialize_fields(result, self.JSON_CLUB_FIELDS)
        return result

    def load_all_clubs_sorted(self, args, element):
        result = self.sql_utils.load_all_documents_sorted("Clubs", args, element)
        for r in result:
            self._deserialize_fields(r, self.JSON_CLUB_FIELDS)
        return result

    def load_all_clubs(self, args):
        result = self.sql_utils.load_all_documents("Clubs", args)
        for r in result:
            self._deserialize_fields(r, self.JSON_CLUB_FIELDS)
        return result

    def delete_club(self, id):
        self.sql_utils.delete_document("Clubs", {"ID": id})
