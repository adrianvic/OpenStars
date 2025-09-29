import pymysql
import datetime
import json
from typing import Optional, Dict, Any, List
import Config
from Utils.Logger import Logger
from Logic.Player import Player
from DataBase.SQLUtils import SQLUtils


class SQLDatabase:
    DEFAULT_PLAYER_DATA: Dict[str, Any] = {
        "ID": 0,
        "token": None,
        "name": "Guest",
        "name_set": False,
        "gems": Player.defaults['gems'],
        "box_tokens": Player.defaults['box_tokens'],
        "big_box_tokens": Player.defaults['big_box_tokens'],
        "coins": Player.defaults['coins'],
        "trophies": Player.defaults['trophies'],
        "tickets": Player.defaults['tickets'],
        "token_doubler": Player.defaults['token_doubler'],
        "highest_trophies": Player.defaults['highest_trophies'],
        "home_brawler": Player.defaults['home_brawler'],
        "trophy_road_reward": Player.defaults['trophy_road_reward'],
        "experience_points": Player.defaults['experience_points'],
        "profile_icon": Player.defaults['profile_icon'],
        "name_color": Player.defaults['name_color'],
        "selected_brawler": Player.defaults['selected_brawler'],
        "region": Player.defaults['region'],
        "supported_content_creator": Player.defaults['supported_content_creator'],
        "starpower": Player.defaults['starpower'],
        "gadget": Player.defaults['gadget'],
        "brawl_pass_activated": Player.defaults['brawl_pass_activated'],
        "welcome_message_viewed": Player.defaults['welcome_message_viewed'],
        "brawlers_unlocked": Player.defaults['brawlers_unlocked'],
        "brawlers_trophies": Player.defaults['brawlers_trophies'],
        "brawlers_highest_trophies": Player.defaults['brawlers_highest_trophies'],
        "brawlers_level": Player.defaults['brawlers_level'],
        "brawlers_power_points": Player.defaults['brawlers_power_points'],
        "unlocked_skins": Player.defaults['unlocked_skins'],
        "selected_skins": Player.defaults['selected_skins'],
        "map_id": Player.defaults['map_id'],
        "use_gadget": Player.defaults['use_gadget'],
        "home_skin": Player.defaults['home_skin'],
        "brawlers_spg": Player.defaults['brawlers_spg'],
        "club_id": Player.defaults['club_id'],
        "club_role": Player.defaults['club_role'],
    }

    DEFAULT_CLUB_DATA: Dict[str, Any] = {
        'ID': 0,
        'name': 'Invalid',
        'description': 'Invalid club.',
        'region': 'BR',
        'badge_id': 0,
        'type': 0,
        'trophies': 0,
        'required_trophies': 0,
        'family_friendly': 0,
        'members': [],
        'messages': []
    }

    JSON_PLAYER_FIELDS = [
        "resources", "brawlers_trophies",
        "brawlers_highest_trophies", "brawlers_level", "brawlers_power_points",
        "unlocked_skins", "selected_skins",
        "leaderboard_data", "delivery_items", "box_rewards",
        "brawlers_unlocked", "brawlers_card_id", "brawlers_spg", "clients"
    ]

    JSON_CLUB_FIELDS = ["members", "messages"]

    def __init__(self):
        self.client = pymysql.connect(
            host=Config.config["DBConnectionURL"],
            user=Config.config["SQLUser"],
            password=Config.config["SQLPassword"],
            database=Config.config["SQLDatabase"],
            cursorclass=pymysql.cursors.DictCursor
        )
        Logger.log("debug", f"Connected to MariaDB {Config.config['SQLDatabase']}")
        self.sql_utils = SQLUtils(self.client)

    # --- Helpers ---
    @staticmethod
    def _serialize_fields(data: dict, fields: List[str]) -> dict:
        for key in fields:
            if key in data and isinstance(data[key], (dict, list)):
                data[key] = json.dumps(data[key])
        return data

    @staticmethod
    def _deserialize_fields(data: dict, fields: List[str]) -> dict:
        for key in fields:
            if key in data and isinstance(data[key], str):
                try:
                    data[key] = json.loads(data[key])
                except json.JSONDecodeError:
                    pass
        return data

    @staticmethod
    def merge(dict1: dict, dict2: dict) -> dict:
        return {**dict1, **dict2}

    # --- Player methods ---
    def create_player_account(self, player_id: int, token: str) -> None:
        Logger.log("debug", f"Creating new player account for ID {player_id}.")
        data = self.merge(self.DEFAULT_PLAYER_DATA, {"ID": player_id, "token": token})
        data = self._serialize_fields(data, self.JSON_PLAYER_FIELDS)
        self.sql_utils.insert_data("Players", data)

    def load_player_account(self, token: str) -> Optional[dict]:
        Logger.log("debug", f"Loading player account for token {token}.")
        result = self.sql_utils.load_document("Players", {"token": token})
        if not result:
            return None
        merged = self.merge(self.DEFAULT_PLAYER_DATA, result)
        merged = self._deserialize_fields(merged, self.JSON_PLAYER_FIELDS)
        return merged

    def load_player_account_by_id(self, player_id: int) -> Optional[dict]:
        Logger.log("debug", f"Loading player account for ID {player_id}.")
        result = self.sql_utils.load_document("Players", {"ID": player_id})
        if result:
            result = self._deserialize_fields(result, self.JSON_PLAYER_FIELDS)
        return result

    def update_player_account(self, token: str, updates: Dict[str, Any]) -> None:
        Logger.log("debug", f"Updating player {token} with keys: {list(updates.keys())}")
        serialized = {}
        for key, value in updates.items():
            if key in self.JSON_PLAYER_FIELDS:
                value = json.dumps(value)
            if key in self.DEFAULT_PLAYER_DATA:
                serialized[key] = value
            else:
                Logger.log("warning", f"Skipped unknown field '{key}'")
        if serialized:
            self.sql_utils.update_document("Players", {"token": token}, serialized)

    # --- Club methods ---
    def create_club(self, club_id: int, data: dict) -> None:
        merged = self.merge(self.DEFAULT_CLUB_DATA, {"ID": club_id})
        print(merged)
        merged.update(data)
        for field in self.JSON_CLUB_FIELDS:
            if field in merged:
                merged[field] = json.dumps(merged[field])
        for k, v in merged.items():
            if isinstance(v, (dict, list)):
                merged[k] = json.dumps(v)
        self.sql_utils.insert_data("Clubs", merged)

    def load_club(self, club_id: int) -> Optional[dict]:
        Logger.log("debug", f"Loading club {club_id}.")
        result = self.sql_utils.load_document("Clubs", {"ID": club_id})
        if not result:
            return self.DEFAULT_CLUB_DATA
        merged = self.merge(self.DEFAULT_CLUB_DATA, result)
        merged = self._deserialize_fields(merged, self.JSON_CLUB_FIELDS)
        return merged

    def delete_club(self, club_id: int):
        """Delete a club by ID"""
        self.sql_utils.delete_data("Clubs", {"id": club_id})

    def update_club(self, club_id: int, updates: dict) -> None:
        Logger.log("debug", f"Updating club {club_id} with keys: {list(updates.keys())}")
        serialized = {k: json.dumps(v) if k in self.JSON_CLUB_FIELDS else v for k, v in updates.items()}
        self.sql_utils.update_document("Clubs", {"id": club_id}, serialized)
