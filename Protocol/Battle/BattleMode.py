import threading
import time
import random
from dataclasses import dataclass
from collections import deque
from Protocol.Battle.GameModeUtils import GameModeUtils
from Protocol.Messages.Server.BattleEndMessage import BattleEndMessage
from Utils.Logger import Logger

# -- warning --
# This is a port of TaleBrawl's BattleMode.cs
# Most of the occurences of player are an instance of BattlePlayer and not Logic.Player!

class BattleMode:
    @dataclass
    class DiedEntry:
        death_tick: int
        player: "BattlePlayer"

    @dataclass
    class Rect:
        x: int
        y: int
        width: int
        height: int
    Update
    @dataclass
    class LogicVector2:
        x: int
        y: int
    
    ORBS_TO_COLLECT_NORMAL = 0xA
    
    # Timer's missing
    client_input

    location_ID: int
    game_mode_variation: int
    player_count_with_variation: int
    players: list[BattlePlayer]
    player_by_sID: dict[int, BattlePlayer]
    player_by_globject: dict[int, BattlePlayer]
    spectators: dict[int, LogicGameListener]
    game_object_manager: GameObjectManager
    play_area: Rect
    game_time: GameTime
    tilemap: m_tileMap
    random: LogicRandom
    random_seed: int
    winner_team: int
    
    dead_players

    players_alive: int
    gem_grab_countdown: int

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    def set_game_over(self, value: bool):
        self.is_game_over = value

    def __init__(self, location_ID):
        self.location_ID = location_ID
        self.winner_team = -1
        self.game_mode_variation = GameModeUtils.get_variation(Location.game_mode) # location?
        self.client_input = deque()

        self.random_seed = 1
        self.random = random.Random(self.m_random_seed)

        self.players = []
        self.player_by_sID = {}
        self.player_by_globject = {}
        self.dead_players = deque()

        self.game_time = GameTime()
        self.tilemap = TileMapFactory.create_tilemap(Location.allowed_maps)
        self.play_area = Rect(0, 0, self.tilemap.logic_width, self.tilemap.logic_height)
        self.game_object_manager = GameObjectManager()

        self.spectators = {}

    def get_gem_grab_countdown(): return self.gem_grab_countdown
    def get_players_alive_battle_royale(): return self.players_alive

    def tick_spawn_heroes():
        entries: DiedEntry = list(self.dead_players)

        for entry in entries:
            if get_ticks_gone() - entry.death_tick < GameModeUtils.get_respawn_seconds(self.game_mode_variation) * 20:
                self.dead_players.append(entry)
                continue
        
        player: BattlePlayer = entry.player
        spawn_point: LogicVector2 = player.get_spawn_point()
        character = Character(16, GlobalID.get_instance_id(player.character_id))
        character.set_index(player.index + (16 * player.tindex))
        character.set_level(player.power_level)
        character.set_bot(player.is_bot)
        character.set_immunity(60, 100)
        self.game_object_manager.add_object(character)
        player.object_ID = character.get_globID
        self.player_by_globject[player.object_ID] = player

    def player_died(player: BattlePlayer):
        if (self.game_mode_variation == 6):
            rank: int = self.players_alive
            self.players_alive -= 1
            player.is_alive = false
            player.battle_royale_rank = rank
            token_rewards: int = 40 / rank

            trophy_reward: int = 0
            
            if rank > 5:
                trophy_reward -= (rank - 5)
            else:
                trophy_reward = (5 - rank) * 2
            

            if player.game_listener == None: return

            message = BattleEndMessage(player.get_client(), player, self.game_mode_variation, 1, players, token_rewards, trophy_reward).send() # uninplemented args // hardcoded end

            # if not player.is_bot:
            #     home_mode: HomeMode = LogicServerListener.instance.get_home_mode(player.account_ID)

            return
        if self.game_mode_variation == 0:
            player.reset_score()

        player.object_ID = 0
        
        entry = DiedEntry()
        entry.player = player
        entry.DeathTick = get_ticks_gone()

        self.dead_players.append(entry)

    def get_player_with_object(global_ID: int) -> BattlePlayer:
        if global_ID in self.player_by_globject:
            return self.player_by_globject[global_ID]
        return None

    def get_tilemap() -> TileMap:
        return self.tilemap
    
    def start():
        threading.Thread(target=update_loop, daemon=True).start()

    def update_loop():
        while True:
            self.update()
            time.sleep(1/20)

    def update():
        self.execute_one_tick()

    def get_player(global_ID: int):
        if global_ID in self.player_by_globject:
            return self.player_by_globject[global_ID]
        return None

    def get_player_with_sid(session_ID: int):
        if session_ID in self.player_by_sID:
            return self.player_by_sID[session_ID]
        return None
    
    def add_spectator(session_ID: int, game_listener: LogicGameListener):
        self.spectators.append(session_ID, game_listener)

    def change_player_sID(old: int, new: int):
        if (old in self.player_by_sID):
            player = self.player_by_sID[old]
            player.last_handled_input = 0
            self.player_by_sID.pop(old)
            self.player_by_sID[new] = player

    def add_player(player: BattlePlayer, session_ID: int):
        if not player == None:
            player.session_ID = session_ID
            self.players.append(player)
            return
            # not feeling like porting player avatar right now

        Logger.log("error", "Protocol.Battle.BattleMode: player is none!")

    def add_game_objects():
        self.players_alive = len(self.players)
        team1_indexer: int = 0
        team2_indexer: int = 0

        for player in self.players:
            character: Character = Character(16, self.global_ID.get_instance_id(player.character_id))
            character.set_index(player.player_index + (16 * player.team_index))
            character.set_level(player.power_level)
            character.set_bot(player.is_bot())
            character.set_immunity(60, 100)

            if GameModeUtils.has_two_teams(self.game_mode_variation):
                if player.team_index == 0:
                    tile: Tile = self.tilemap.spawn_points_team1[team1_indexer]
                    team1_indexer += 1
                    character.set_position(tile.x, tile.y, 0)
                    player.set_spawn_point(tile.x, tile.y)
                else:
                    tile: Tile = self.tilemap.spawn_points_team2[team2_indexer]
                    team2_indexer += 1
                    character.set_position(tile.x, tile.y, 0)
                    player.set_spawn_point(tile.x, tile.y)
            else:
                tile: Tile = self.tilemap.spawn_points_team1[team1_indexer]
                team1_indexer += 1
                character.set_position(tile.x, tile.y, 0)
                player.set_spawn_point(tile.x, tile.y)

            self.game_object_manager.add_game_object(character)
            player.object_ID = character.get_globID
            self.player_by_globject.append(player.object_ID, player)

        if self.game_mode_variation == 0:
            data: ItemData = DataTables.get(18).get_data("OrbSpawner")
            item = Item(18, data.get_instance_id())
            item.set_position(2950, 4950)
            item.disable_appear_animation()
            self.game_object_manager.add_game_object(item)
        
        if self.game_mode_variation == 3:
            data: ItemData = DataTables.get(18).get_data("Money")
            item = Item(18, data.get_instance_id())
            item.set_position(2950, 4950)
            item.disable_appear_animation()
            self.game_object_manager.add_game_object(item)

        if self.game_mode_variation == 6:
            data: CharacterData = DataTables.get(16).get_data("Lootbox")
            for i in range(self.tilemap.height):
                for j in range(self.tilemap.width):
                    tile: Tile = self.tilemap.get_tile(i, j, true)
                    if tile.code == '4':
                        should_spawn_box = get_random_int(0, 120) < 60
                        if should_spawn_box:
                            box = Character(16, data.get_instance_id())
                            box.set_position(tile.X, tile.Y)
                            self.game_object_manager.add_game_object(box)
        
        instance_ID: int = DataTables.get(16).get_instance_id("LaserBall")
        gem = Character(16, instance_ID)
        gem.set_position(2950 + 450, 4950 - 333, 0)
        # self.game_object_manager.add_game_object(gem)

    def remove_spectator(id: int):
        if id not in self.spectators: return
        self.spectators.pop(id)

    def is_in_play_area(x: int, y: int):
        return self.play_area.is_inside(x, y)

    def get_team_players_count(team_index: int) -> int:
        result = 0
        for player in get_players():
            if player.team_index == team_index: result += 1
        return result

    def add_client_input(input: ClientInput, session_ID: int):
        if session_ID not in self.player_by_sID: return # maybe should call values()

        input.owner_session_id = session_ID
        self.input_queue.append(input)

    def handle_spectator_input(input: ClientInput, session_ID: int):
        if input is None: return
        if session_ID not in self.spectators: return

        self.spectators[session_ID].handled_inputs = input.index

    def handle_client_input(input: ClientInput):
        if input is None: return

        player: BattlePlayer = self.get_player_with_sid(input_owner_sid)

        if player is None: return
        if player.last_handled_input >= input.index: return

        player.last_handled_input = input.index

        if input.type == 0:
            character: Character = self.game_object_manager.object_by_ID(player.object_ID)
            if character is None: return

            skill: Skill = character.get_weapon_skill()
            if character is None: return

            character.ulti_disabled()

            indirection = false

            if skill.skill_data.projectile is not Null:
                projectile_data: ProjectileData = DataTables.get(DataType.projectile).get_data(skill.skill_data.projectile)
                indirection.projectile_data.indirect

            # if not input.auto_attack and not indirection:
            # I'll continue tomorrow

    def get_random_int(a: int, b: int) -> int:
        return random.randrange(a, b)