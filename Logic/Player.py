import copy
import json
import Config
from Utils.Logger import Logger
from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters
from Files.CsvLogic.Skins import Skins
from Utils.Fingerprint import Fingerprint

class DirtyList(list):
    def __init__(self, player, key, iterable=None):
        super().__init__(iterable if iterable else [])
        self._player = player
        self._key = key

    def _mark_dirty(self):
        self._player._dirty.add(self._key)
        self._player.save()

    def append(self, item):
        super().append(item)
        self._mark_dirty()

    def extend(self, iterable):
        super().extend(iterable)
        self._mark_dirty()

    def __setitem__(self, idx, value):
        super().__setitem__(idx, value)
        self._mark_dirty()

    def __delitem__(self, idx):
        super().__delitem__(idx)
        self._mark_dirty()

class DirtyDict(dict):
    def __init__(self, player, key, initial=None):
        super().__init__(initial if initial else {})
        self._player = player
        self._key = key

    def _mark_dirty(self):
        self._player._dirty.add(self._key)
        self._player.save()

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        self._mark_dirty()

    def __delitem__(self, k):
        super().__delitem__(k)
        self._mark_dirty()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._mark_dirty()


class Player:
    skins_id = Skins().get_skins_id()
    brawlers_id = Characters().get_brawlers_id()

    defaults = {
        "ID": 0,
        "token": None,
        "trophies": Config.config.get("Trophies", 0),
        "tickets": Config.config.get("Tickets", 0),
        "gems": Config.config.get("Gems", 0),
        "box_tokens": Config.config.get("box_tokens", 0),
        "big_box_tokens": Config.config.get("big_box_tokens", 0),
        "coins": Config.config.get("coins", 0),
        "highest_trophies": Config.config.get("Trophies", 0),
        "trophy_road_reward": 1,
        "experience_points": Config.config.get("ExperiencePoints", 0),
        "profile_icon": 0,
        "name_color": 0,
        "selected_brawler": 0,
        "region": Config.config.get("Region", "BR"),
        "supported_content_creator": "Classic Brawl",
        "name_set": False,
        "name": "Guest",
        "map_id": 0,
        "use_gadget": True,
        "starpower": 76,
        "gadget": 255,
        "home_brawler": 0,
        "home_skin": 0,
        "brawl_pass_activated": False,
        "token_doubler": 0,
        "welcome_message_viewed": False,
        "unlocked_skins": [],
        "selected_skins": {str(b): 0 for b in brawlers_id},
        "brawlers_unlocked": [0, 1],
        "brawlers_spg": Cards().get_spg_id(),
        "brawlers_trophies": {str(b): 0 for b in brawlers_id},
        "brawlers_highest_trophies": {str(b): 99999 for b in brawlers_id},
        "brawlers_level": {str(b): 0 for b in brawlers_id},
        "brawlers_power_points": {str(b): 0 for b in brawlers_id},
        "club_id": 0,
        "club_role": 0,
        "token_rewards": 0,
    }

    _volatile = {
        "theme_id": Config.config.get("ThemeID", 1),
        "content_creator_codes": Config.config.get("ContentCreatorCodes", ""),
        "maintenance": Config.config.get("Maintenance", False),
        "maintenance_time": Config.config.get("SecondsTillMaintenanceOver", 3600),
        "patch": Config.config.get("Patch", False),
        "patch_url": Config.config.get("PatchURL", "http://192.168.0.103:8080/"),
        "patch_sha": Fingerprint.loadFinger("GameAssetsReplication/fingerprint.json"),
        "update_url": Config.config.get("UpdateURL", ""),
        "clubWarsEnabled": Config.config.get("ClubWarsEnabled", False),
        "leaderboardData": [],
        "box_rewards": {},
        "delivery_items": {},
        "message_tick": 0,
        "clients": {},
        "battle_tick": 0,
        "status": 0,
    }

    def __init__(self, player_id=0, db=None, data=None):
        self._data = {}
        self._db = db
        self._suspend_save = False
        self._dirty = set()

        # Deepcopy defaults
        for k, v in self.defaults.items():
            self._data[k] = copy.deepcopy(v)

        # Wrap mutable fields with dirty-tracking wrappers
        self._wrap_mutables()

        self._data["ID"] = player_id

        if data:
            self.load_from_data(data)

    def _wrap_mutables(self):
        # Lists
        self._data["brawlers_unlocked"] = DirtyList(self, "brawlers_unlocked", self._data["brawlers_unlocked"])
        self._data["unlocked_skins"] = DirtyList(self, "unlocked_skins", self._data["unlocked_skins"])

        # Dicts
        self._data["brawlers_level"] = DirtyDict(self, "brawlers_level", self._data["brawlers_level"])
        self._data["brawlers_trophies"] = DirtyDict(self, "brawlers_trophies", self._data["brawlers_trophies"])
        self._data["brawlers_power_points"] = DirtyDict(self, "brawlers_power_points", self._data["brawlers_power_points"])
        self._data["selected_skins"] = DirtyDict(self, "selected_skins", self._data["selected_skins"])

    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]
        elif key in self._volatile:
            return self._volatile[key]
        raise AttributeError(f"{key} not found")

    def __setattr__(self, key, value):
        if key in ("_data", "_db", "_suspend_save", "_dirty"):
            super().__setattr__(key, value)
            return
        if key in self._data:
            self._data[key] = value
            if not self._suspend_save and self._db:
                self._dirty.add(key)
                self.save()
        else:
            super().__setattr__(key, value)

    def save(self):
        if self._db and self._dirty:
            data_to_save = {k: self._data[k] for k in self._dirty if k not in self._volatile}
            if data_to_save:
                self._db.update_player_account(self._data["token"], data_to_save)
            self._dirty.clear()

    def load_from_data(self, data):
        self._suspend_save = True
        try:
            for key, value in data.items():
                if key in self._data:
                    self._data[key] = value
        finally:
            self._suspend_save = False

    def load_from_db(self):
        if self._db:
            data = self._db.load_player_account_by_id(self.ID)
            if data:
                self.load_from_data(data)

    def to_dict(self):
        return dict(self._data.items())

    def __repr__(self):
        return f"<Player ID={self.ID}, Name={self.name}>"

    @property
    def brawlers_card_id(self):
        return [Cards().get_unlock_by_brawler_id(b) for b in self.brawlers_unlocked]

    def get_resources(self):
        return  [
            {"ID": 1, "Amount": self.box_tokens},
            {"ID": 8, "Amount": self.coins},
            {"ID": 9, "Amount": self.big_box_tokens},
            {"ID": 10, "Amount": 0} # star points
        ]

    def reward_token(amount: int):
        self._data.token_rewards += amount
        self._data.box_tokens += amount

    def token_rewards_seen():
        self._data.token_rewards = 0