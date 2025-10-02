
import json
from Logic.Player import Player
from Logic.Battle.Structures.PlayerKilledEntry import PlayerKilledEntry
from Logic.Data.DataTables import DataTables
from Utils.Helpers import Helpers
from ByteStream.Writer import Writer
from ByteStream.Reader import Reader
from Math.LogicVector2 import LogicVector2
# using Supercell.Laser.Titan.DataStream;
from Math import *
from typing import List

class DisplayData:
    def __init__(self):
        self.name = None
        self.name_color = None
        self.thumbnail_id = None

class BattlePlayer:
    def __init__(self, player_index: int, team_index: int, player: Player = None, is_bot: bool = False, name: str = "noname", character: int = 0):
        self.display_data = DisplayData()
        
        if is_bot:
            self.display_data.name = name
            self.display_data.name_color_id = 0 # placeholder
            self.display_data.thumbnail_id = 0 # placeholder
            self.account_id = 100000 + player_index
            self.character = character
            self.session_id = -1

        else:
            self.display_data.thumbnail_id = player.profile_icon
            self.display_data.name_color_id = player.name_color
            self.avatar = player
            self.account_id = player.ID
            self.trophies: int = player.brawlers_trophies[character]
            self.highest_trophies = player.brawlers_highest_trophies[character]
            self.power_level = player.brawlers_level[character]
            self.player_display_data = player.display
            self.character_id = player.home_brawler

        self.team_index = team_index
        self.player_index = player_index
        self.bot = is_bot
        
        self.is_star_player: bool = False
        self.team_id: int = None
        self.skin_id: int = None
        self.session_id: int = None
        self.logic_game_listener: GameListener = None
        self.own_object_id = None
        self.last_handled_input: int = None
        self.power_play_score: int = None
        self.hero_power_level: int = None
        self.score: int = 0
        self.start_using_pin_tick: int = None
        self.pin_index: int = None
        self.ulti_charge: int = None
        self.is_alive: bool = None
        self.battle_royale_rank = -1
        self.kill_list = []
        self.kills: int = 0
        self.damage: int = 0
        self.heals: int = 0
        self.spawn_point = LogicVector2()
        self.start_using_pin_ticks = -9999
        self.hero_power_level = 0
        self.is_alive = True
        self.kill_list: List[PlayerKillEntry] = []
    
    def healed(self, heals: int):
        self.heals += heals

    def damage_dealed(self, damage: int):
        self.damage += damage

    def killed_player(self, index: int, bounty_stars: int):
        self.kill_list.append(PlayerKillEntry(index, bounty_stars))
        self.kills += 1

    def has_ulti(self) -> bool: return self.ulti_charge >= 4000

    def get_ulti_charge(self): return self.ulti_charge

    def add_ulti_charge(self, amount: int):
        self.ulti_charge = min(4000, (self.ulti_charge or 0) + amount)

    #def add_ulti_charge(self, amount: int): self.ulti_charge = min(4000, ulti_charge + amount) # take a look

    def use_ulti(self): self.ulti_charge = 0

    def is_bot(self) -> bool: return self.bot

    def add_score(self, a: int):
        self.score += a

    def reset_score(self):
        self.score = 0

    def use_pin(self, index: int, ticks: int):
        self.start_using_pin_ticks = ticks
        self.pin_index = index

    def is_using_pin(self, ticks: int) -> bool: return (ticks - self.start_using_pin_ticks) < 80

    def get_pin_index(self): return self.pin_index

    def get_pin_use_cooldown(self, ticks: int): return self.start_using_pin_ticks + 100

    def get_score(self): return self.score

    def set_spawn_point(self, x: int, y: int): self.spawn_point.set(x, y)

    def get_spawn_point(self) -> LogicVector2: return self.spawn_point.clone()

    # def decode(self, stream: ByteStream):
    #     self.character_id = Reader.readDataReference(stream)
    #     self.skin_id = Reader.readDataReference(stream)
    #     self.team_index = Reader.ReadVInt(stream) # take a look at this
    #     self.bot = not Reader.ReadBoolean(stream)
    #     self.display_data.name = Reader.ReadString(stream)

    # def encode(self, stream: ByteStream):
    #     stream.WriteLong(self.account_id)
    #     stream.WriteVInt(self.player_index)
    #     stream.WriteVInt(self.team_index)
    #     stream.WriteVInt(0)
    #     stream.WriteInt(0)
    #     Writer.writeDataReference(stream, self.character_id)
    #     Writer.writeDataReference(stream, None)
    #     stream.WriteBoolean(False)
    #     stream.WriteBoolean(False)
    #     self.display_data.encode(stream)