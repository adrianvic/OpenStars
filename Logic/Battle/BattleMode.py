import threading
import time
import random
from dataclasses import dataclass
from collections import deque
from Logic.Battle.GameModeUtils import GameModeUtils
from Protocol.Messages.Server.BattleEndMessage import BattleEndMessage
from Logic.Battle.Structures.BattlePlayer import BattlePlayer
from Logic.Battle.Level.TileMap import TileMap
from Utils.Logger import Logger
from Logic.Data.DataTables import DataTables
from Logic.Data.DataType import DataType
from concurrent.futures import ThreadPoolExecutor
from Logic.LogicGameListener import LogicGameListener
from Logic.Battle.Input.ClientInput import ClientInput
from Logic.Data.LocationData import LocationData

# -- warning --
# This is a port of TaleBrawl's BattleMode.cs
# Most of the occurences of player are an instance of BattlePlayer and not Logic.Player!

class BattleMode:
    ORBS_TO_COLLECT_NORMAL = 10

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    def set_game_over(self, value: bool):
        self._is_game_over = value

    def __init__(self, location_id: int):
        self._location_id = location_id
        self._winner_team = -1

        # Game mode and player count
        self._game_mode_variation = GameModeUtils.get_variation(self.location.game_mode)
        self._players_count_with_variation = GamePlayUtil.get_player_count_with_variation(
            self._game_mode_variation
        )

        # Queues and timers
        self._input_queue = deque()
        self._dead_players = deque()
        self._update_timer = None

        # Players
        self._players: list[BattlePlayer] = []
        self._players_by_session_id: dict[int, BattlePlayer] = {}
        self._players_by_object_global_id: dict[int, BattlePlayer] = {}
        self._spectators: dict[int, LogicGameListener] = {}

        # Game objects
        self._game_object_manager = GameObjectManager(self)
        self._tile_map = TileMapFactory.create_tile_map(self.location.allowed_maps)
        self._play_area = Rect(0, 0, self._tile_map.logic_width, self._tile_map.logic_height)

        # Timing and randomness
        self._time = GameTime()
        self._random_seed = 0
        self._random = LogicRandom(self._random_seed)

        # Game state
        self._running = True
        self._players_alive = 0
        self._gem_grab_countdown = 0
        self.is_game_over = False
        self.id: int = 0

    def get_gem_grab_countdown(self): return self.gem_grab_countdown
    def get_players_alive_battle_royale(self): return self.players_alive

    def tick_spawn_heroes(self):
        entries: DiedEntry = list(self.dead_players)

        for entry in entries:
            if get_ticks_gone() - entry.death_tick < GameModeUtils.get_respawn_seconds(self.game_mode_variation) * 20:
                self.dead_players.append(entry)
                continue
            player: BattlePlayer = entry.player
            spawn_point: LogicVector2 = player.get_spawn_point()
            character = Character(16, GlobalID.get_instance_id(player.character_id), self)
            character.set_index(player.index + (16 * player.tindex))
            character.set_level(player.power_level)
            character.set_bot(player.bot)
            character.set_immunity(60, 100)
            self.game_object_manager.add_game_object(character)
            player.own_object_id = character.get_globID
            self.player_by_globject[player.own_object_id] = player

    def player_died(self, player: BattlePlayer):
        if (self.game_mode_variation == 6):
            rank: int = self.players_alive
            self.players_alive -= 1
            player.is_alive = False
            player.battle_royale_rank = rank
            token_rewards: int = 40 / rank

            trophy_reward: int = 0
            
            if rank > 5:
                trophy_reward -= (rank - 5)
            else:
                trophy_reward = (5 - rank) * 2
            

            if player.game_listener == None: return

            message = BattleEndMessage(player.get_client(), player, self.game_mode_variation, 1, players, token_rewards, trophy_reward).send() # uninplemented args // hardcoded end

            if not player.bot:
                home_mode: HomeMode = LogicServerListener.instance.get_home_mode(player.account_ID)

            return
        if self.game_mode_variation == 0:
            player.reset_score()

        player.own_object_id = 0
        
        entry = DiedEntry()
        entry.player = player
        entry.death_tick = get_ticks_gone()

        self.dead_players.append(entry)

    def get_player_with_object(self, global_ID: int) -> BattlePlayer:
        if global_ID in self.player_by_globject:
            return self.player_by_globject[global_ID]
        return None

    def get_tilemap(self) -> TileMap:
        return self.tilemap
    
    def start(self):
        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        while self._running:
            self.update()
            time.sleep(1/20)

    def update(self):
        self.execute_one_tick()

    def get_player(self, global_ID: int):
        if global_ID in self.player_by_globject:
            return self.player_by_globject[global_ID]
        return None

    def get_player_by_sid(self, session_ID: int):
        if session_ID in self.player_by_sID:
            return self.player_by_sID[session_ID]
        return None
    
    def add_spectator(self, session_ID: int, game_listener: LogicGameListener):
        self.spectators[session_ID] = game_listener

    def change_player_sID(self, old: int, new: int):
        if (old in self.player_by_sID):
            player = self.player_by_sID[old]
            player.last_handled_input = 0
            self.player_by_sID.pop(old)
            self.player_by_sID[new] = player

    def add_player(self, player: BattlePlayer, session_ID: int):
        if not player == None:
            player.session_ID = session_ID
            self.players.append(player)
            return
            # not feeling like porting player avatar right now

        Logger.log("error", "Protocol.Battle.BattleMode: player is none!")

    def add_game_object(self):
        self.players_alive = len(self.players)
        team1_indexer: int = 0
        team2_indexer: int = 0

        for player in self.players:
            character: Character = Character(16, self.global_ID.get_instance_id(player.character_id), self)
            character.set_index(player.player_index + (16 * player.team_index))
            character.set_level(player.power_level)
            character.set_bot(player.bot)
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
            player.own_object_id = character.get_globID
            self.player_by_globject[player.own_object_id] = player

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
                    tile: Tile = self.tilemap.get_tile(i, j, True)
                    if tile.code == '4':
                        should_spawn_box = get_random_int(0, 120) < 60
                        if should_spawn_box:
                            box = Character(16, data.get_instance_id(), self)
                            box.set_position(tile.X, tile.Y)
                            self.game_object_manager.add_game_object(box)
        
        instance_ID: int = DataTables.get(16).get_instance_id("LaserBall")
        gem = Character(16, instance_ID, self)
        gem.set_position(2950 + 450, 4950 - 333, 0)
        # self.game_object_manager.add_game_object(gem)

    def remove_spectator(self, id: int):
        if id not in self.spectators: return
        self.spectators.pop(id)

    def is_in_play_area(self, x: int, y: int):
        return self.play_area.is_inside(x, y)

    def get_team_players_count(self, team_index: int) -> int:
        result = 0
        for player in get_players():
            if player.team_index == team_index: result += 1
        return result

    def add_client_input(self, input: ClientInput, session_ID: int):
        if session_ID not in self.player_by_sID: return # maybe should call values()

        input.owner_session_id = session_ID
        self.input_queue.append(input)

    def handle_spectator_input(self, input: ClientInput, session_ID: int):
        if input is None: return
        if session_ID not in self.spectators: return

        self.spectators[session_ID].handled_inputs = input.index

    def handle_client_input(self, input: "ClientInput"):
        if input is None:
            return

        player: BattlePlayer = self.get_player_by_sid(input.owner_session_id)
        if player is None:
            return
        if player.last_handled_input >= input.index:
            return

        player.last_handled_input = input.index

        if input.type == 0:
            character: Character = self.game_object_manager.get_object_by_id(player.own_object_id, self)
            if character is None:
                return

            skill: Skill = character.get_weapon_skill()
            if skill is None:
                return

            character.ulti_disabled()

            indirection = False
            if skill.skill_data.projectile is not None:
                projectile_data: "ProjectileData" = DataTables.get(DataType.PROJECTILE).get_data(skill.skill_data.projectile)
                indirection = projectile_data.indirect

            if not input.auto_attack and not indirection:
                character.activate_skill(False, input.x, input.y)
            else:
                character.activate_skill(False, input.x - character.get_x(), input.y - character.get_y())

        elif input.type == 1:
            character: "Character" = self.game_object_manager.get_object_by_id(player.own_object_id, self)
            if character is None:
                return

            skill: "Skill" = character.get_ultimate_skill()
            if skill is None:
                return

            if not player.has_ulti():
                return
            player.use_ulti()

            character.ulti_enabled()

            indirection = False
            if skill.skill_data.projectile is not None:
                projectile_data: "ProjectileData" = DataTables.get(DataType.PROJECTILE).get_data(skill.skill_data.projectile)
                indirection = projectile_data.indirect

            if not input.auto_attack and not indirection:
                character.activate_skill(True, input.x, input.y)
            else:
                character.activate_skill(True, input.x - character.get_x(), input.y - character.get_y())

        elif input.type == 2:
            character: "Character" = self.game_object_manager.get_object_by_id(player.own_object_id, self)
            if character is None:
                return

            character.move_to(input.x, input.y)

        elif input.type == 5:
            character: "Character" = self.game_object_manager.get_object_by_id(player.own_object_id, self)
            if character:
                character.ulti_enabled()

        elif input.type == 6:
            character: "Character" = self.game_object_manager.get_object_by_id(player.own_object_id, self)
            if character:
                character.ulti_disabled()

        else:
            Logger.log("warning", f"Input is unhandled: {input.type}")

    def is_tile_on_poison_area(self, xtile: int, ytile: int) -> bool:
        if self.game_mode_variation != 6: return False
        tick: int = get_ticks_gone()
        if tick > 500:
            poisons = 0
            poisons += (tick - 500) / 100

            if xtile <= poisons or xtile >= 59 - poisons or ytile <= poisons or ytile >= 59 - poisons: return True
        return False

    def handle_incoming_input_messages(self):
        while self.input_queue:
            self.handle_client_input(self.input_queue.popleft())
        
    def execute_one_tick(self):
        try:
            self.handle_incoming_input_messages()
            for player in get_players():
                player.kill_list.clear()
            
            if self.calculate_is_game_over():
                self._running = False
                self.game_over()
                self.is_game_over = True
                return

            self.game_object_manager.pre_tick()
            self.tick()
            self.game_time.increase_tick()
            self.send_vision_update()

        except Exception as e:
            Logger.log("error", f"Battle stopped with exception: {e}")
            self._running = False
            self.is_game_over = True

    def ticK_spawn_event_stuff_delayed(self):
        if self.game_mode_variation == 0:
            if self.ticks_gone() % 100 == 0:
                instance_id = DataTables.get(18).GetInstanceId("Point")
                gem = Item(18, instance_id)
                gem.set_position(2950, 4950, 0)
                gem.set_angle(self.get_random_int(0, 360))
                self.game_object_manager.add_game_object(gem)

    def game_over(self):
        self.send_battle_end()

    def send_battle_end(self):
        for player in self.players:
            if player.session_id < 0:
                continue
            if not player.is_alive:
                continue
            if player.battle_royale_rank == -1:
                player.battle_royale_rank = 1
            if player.avatar is None:
                continue

            rank = player.battle_royale_rank
            player.avatar.BattleId = -1
            is_victory = self.winner_team == player.TeamIndex

            message = BattleEndMessage()
            hero = player.avatar.get_hero(player.CharacterId)

            if not player.bot():
                home_mode = self.LogicServerListener.instance().get_home_mode(player.account_id)
                if home_mode and home_mode.home.quests:
                    message.progressive_quests = home_mode.home.quests.update_quests_progress(
                        self.game_mode_variation, player.character_id,
                        player.kills, player.damage, player.heals, home_mode.home
                    )

            if self.game_mode_variation != 6:
                message.game_mode = 1
                message.is_pvp = True
                message.players = self.players
                message.own_player = player

                if self.winner_team == -1:  # Draw
                    message.result = 2
                    message.tokens_reward = 10
                    message.trophies_reward = 0
                    player.reward_token(10)

                elif is_victory:
                    message.result = 0
                    message.tokens_reward = 20
                    trophies_reward = random.randint(5, 7) + 1
                    message.trophies_reward = trophies_reward
                    hero.add_trophies(trophies_reward)
                    player.avatar.trio_wins += 1
                    player.reward_token(10)
                    player.home.trophies_reward = max(player.home.trophies_reward + trophies_reward, 0)

                else:
                    message.result = 1
                    message.tokens_reward = 10
                    trophies_reward = -2
                    if hero.Trophies < -trophies_reward:
                        trophies_reward = -hero.Trophies
                    message.trophies_reward = trophies_reward
                    hero.add_trophies(trophies_reward)
                    player.reward_token(10)
                    player.home.trophies_reward = max(player.home.trophies_reward + trophies_reward, 0)

            else:  # Battle Royale mode
                message.is_pvp = True
                message.game_mode = 2
                message.result = rank
                message.players = [player]
                message.own_player = player

                tokens_reward = 40 // rank
                message.tokens_reward = tokens_reward

                if rank > 5:
                    trophies_reward = -(rank - 5)
                    if hero.Trophies < -trophies_reward:
                        trophies_reward = -hero.Trophies
                    message.trophies_reward = trophies_reward
                    player.reward_token(tokens_reward)
                    hero.add_trophies(trophies_reward)

                else:
                    trophies_reward = (5 - rank) * 2
                    message.trophies_reward = trophies_reward
                    player.reward_token(tokens_reward)
                    player.home.trophies_reward += trophies_reward

                    if rank <= 4:
                        player.avatar.add_star_tokens(1)
                        message.star_roken = True
                        player.home.star_token_reward += 1

                    hero.add_trophies(trophies_reward)

            if player.avatar is None or player.game_listener is None:
                continue
            player.game_listener.send_tcp_message(message)

    def get_team_score(self, team: int) -> int:
        score = 0
        for player in self.players:
            if (player.team_index == team): score += player.get_score()
        return score

    def calculate_is_game_over(self) -> bool:
        ticks_gone = self.get_ticks_gone()

        if self.game_mode_variation == 3:
            if ticks_gone >= 20 * 120 + 120:
                if self.get_team_score(0) > self.get_team_score(1):
                    self.winner_team = 0
                elif self.get_team_score(0) < self.get_team_score(1):
                    self.winner_team = 1
                else:
                    self.winner_team = -1
                return True

        elif self.game_mode_variation == 0:
            team0_score = self.get_team_score(0)
            team1_score = self.get_team_score(1)

            if team0_score > team1_score and team0_score >= 10:
                if self.gem_grab_countdown == 0:
                    self.gem_grab_countdown = ticks_gone + 20 * 17
                elif ticks_gone > self.gem_grab_countdown:
                    self.winner_team = 0
                    return True

            elif team0_score < team1_score and team1_score >= 10:
                if self.gem_grab_countdown == 0:
                    self.gem_grab_countdown = ticks_gone + 20 * 17
                elif ticks_gone > self.gem_grab_countdown:
                    self.winner_team = 1
                    return True

            else:
                self.gem_grab_countdown = 0

        elif self.game_mode_variation == 6:
            if self.players_alive <= 1:
                return True

        return False

    def tick(self):
        self.tick_spawn_event_stuff_delayed()
        self.game_object_manager.tick()
        self.tick_spawn_heroes()

    def send_vision_update(self):
        def update_player_vision(player):
            if player.game_listener is not None:
                vision_bit_stream = BitStream(64)
                self.game_object_manager.encode(
                    vision_bit_stream, self.tilemap,
                    player.own_object_id, player.player_index, player.team_index
                )

                vision_update = self.vision_update_message()
                vision_update.tick = self.get_ticks_gone()
                vision_update.handled_inputs = player.last_handled_input
                vision_update.viewers = len(self.spectators)
                vision_update.vision_bit_stream = vision_bit_stream

                player.game_listener.send_message(vision_update)

        # Parallel update for all players
        with ThreadPoolExecutor() as executor:
            executor.map(update_player_vision, self.players)

        # Prepare spectate stream
        spectate_stream = BitStream(64)
        self.game_object_manager.encode(spectate_stream, self.tilemap, 0, -1, -1)

        # Send updates to spectators in a separate thread
        def update_spectators():
            for game_listener in list(self.spectators.values()):
                vision_update = vision_update_message()
                vision_update.tick = self.get_ticks_gone()
                vision_update.handled_inputs = game_listener.handled_inputs
                vision_update.viewers = len(self.spectators)
                vision_update.vision_bit_stream = spectate_stream

                game_listener.send_message(vision_update)

        threading.Thread(target=update_spectators).start()

    def get_players(self):
        return self.players.values()

    def get_random_int(self, a: int, b: int) -> int:
        return random.randrange(a, b)

    def get_ticks_gone(self) -> int:
            return self.time.get_tick()
    
    @property
    def location(self) -> LocationData:
        return DataTables.get(DataType.LOCATION).get_by_global_id(self._location_id)