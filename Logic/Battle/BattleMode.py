import threading
import time
import random
from dataclasses import dataclass
from collections import deque
from Protocol.Battle.GameModeUtils import GameModeUtils
from Protocol.Messages.Server.BattleEndMessage import BattleEndMessage
from Logic.Battle.Structures.BattlePlayer import BattlePlayer
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
        self._is_game_over = value

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
        self.game_object_manager.add_game_object(character)
        player.object_ID = character.get_globID
        self.player_by_globject[player.object_ID] = player

    def player_died(player: BattlePlayer):
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

    def get_player_by_sid(session_ID: int):
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

    def add_game_object():
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
                    tile: Tile = self.tilemap.get_tile(i, j, True)
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

    def handle_client_input(self, input: "ClientInput"):
        if input is None:
            return

        player: "BattlePlayer" = self.get_player_with_sid(input.owner_session_id)
        if player is None:
            return
        if player.last_handled_input >= input.index:
            return

        player.last_handled_input = input.index

        if input.type == 0:
            character: "Character" = self.game_object_manager.get_object_by_id(player.object_ID)
            if character is None:
                return

            skill: "Skill" = character.get_weapon_skill()
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
            character: "Character" = self.game_object_manager.get_object_by_id(player.object_ID)
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
            character: "Character" = self.game_object_manager.get_object_by_id(player.object_ID)
            if character is None:
                return

            character.move_to(input.x, input.y)

        elif input.type == 5:
            character: "Character" = self.game_object_manager.get_object_by_id(player.object_ID)
            if character:
                character.ulti_enabled()

        elif input.type == 6:
            character: "Character" = self.game_object_manager.get_object_by_id(player.object_ID)
            if character:
                character.ulti_disabled()

        else:
            Logger.log("warning", f"Input is unhandled: {input.type}")

    def is_tile_on_poison_area(xtile: int, xtile: int) -> bool:
        if self.game_mode_variation != 6: return False
        tick: int = get_ticks_gone()
        if tick > 500:
            poisons = 0
            poisons += (tick - 500) / 100

            if xtile <= poisons || xtile >= 59 - poisons || ytile <= poisons || ytile >= 59 - poisons: return True
        return False

    def handle_incoming_input_messages(self):
        while self.input_queue.count > 0:
            this.HandleClientInput(self.input_queue.popleft())
        
    def execute_one_tick():
        try:
            self.handle_incoming_input_messages()
            for player in get_players():
                player.kill_list.clear()
            
            if self.calculate_is_game_over():
                self.update_timer.cancel()
                self.game_over()
                self.is_game_over = True
                return

            self.game_object_manager.pre_tick()
            self.tick()
            self.game_time.increase_tick()
            self.send_vision_update()

        except Exception as e:
            Logger.log("error", f"Battle stopped with exception: {e}")
            self.update_timer.cancel()
            self.is_game_over = True

    def ticK_spawn_event_stuff_delayed():
        if self.game_mode_variation == 0:
            if self.ticks_gone() % 100 == 0
                instance_id = DataTables.get(18).GetInstanceId("Point")
                gem = Item(18, instance_id)
                gem.set_position(2950, 4950, 0)
                gem.set_angle(self.get_random_int(0, 360))
                self.game_object_manager.add_game_object(gem)

    def game_over():
        self.send_battle_end()

    def send_battle_end():
        for player in self.m_players:
            if player.SessionId < 0:
                continue
            if not player.IsAlive:
                continue
            if player.BattleRoyaleRank == -1:
                player.BattleRoyaleRank = 1
            if player.Avatar is None:
                continue

            rank = player.BattleRoyaleRank
            player.Avatar.BattleId = -1
            is_victory = self.m_winnerTeam == player.TeamIndex

            message = BattleEndMessage()
            hero = player.Avatar.get_hero(player.CharacterId)

            if not player.is_bot():
                home_mode = LogicServerListener.instance().get_home_mode(player.AccountId)
                if home_mode and home_mode.Home.Quests:
                    message.ProgressiveQuests = home_mode.Home.Quests.update_quests_progress(
                        self.m_gameModeVariation, player.CharacterId,
                        player.Kills, player.Damage, player.Heals, home_mode.Home
                    )

            if self.m_gameModeVariation != 6:
                message.GameMode = 1
                message.IsPvP = True
                message.Players = self.m_players
                message.OwnPlayer = player

                if self.m_winnerTeam == -1:  # Draw
                    message.Result = 2
                    message.TokensReward = 10
                    message.TrophiesReward = 0
                    player.Avatar.add_tokens(10)
                    player.Home.TokenReward += 10

                elif is_victory:
                    message.Result = 0
                    message.TokensReward = 20
                    trophies_reward = random.randint(5, 7) + 1
                    message.TrophiesReward = trophies_reward
                    hero.add_trophies(trophies_reward)
                    player.Avatar.add_tokens(20)
                    player.Avatar.TrioWins += 1
                    player.Home.TokenReward += 20
                    player.Home.TrophiesReward = max(player.Home.TrophiesReward + trophies_reward, 0)

                else:
                    message.Result = 1
                    message.TokensReward = 10
                    trophies_reward = -2
                    if hero.Trophies < -trophies_reward:
                        trophies_reward = -hero.Trophies
                    message.TrophiesReward = trophies_reward
                    hero.add_trophies(trophies_reward)
                    player.Avatar.add_tokens(10)
                    player.Home.TokenReward += 10
                    player.Home.TrophiesReward = max(player.Home.TrophiesReward + trophies_reward, 0)

            else:  # Battle Royale mode
                message.IsPvP = True
                message.GameMode = 2
                message.Result = rank
                message.Players = [player]
                message.OwnPlayer = player

                tokens_reward = 40 // rank
                message.TokensReward = tokens_reward

                if rank > 5:
                    trophies_reward = -(rank - 5)
                    if hero.Trophies < -trophies_reward:
                        trophies_reward = -hero.Trophies
                    message.TrophiesReward = trophies_reward
                    player.Avatar.add_tokens(tokens_reward)
                    player.Home.TokenReward += tokens_reward
                    hero.add_trophies(trophies_reward)

                else:
                    trophies_reward = (5 - rank) * 2
                    message.TrophiesReward = trophies_reward
                    player.Avatar.add_tokens(tokens_reward)
                    player.Home.TokenReward += tokens_reward
                    player.Home.TrophiesReward += trophies_reward

                    if rank <= 4:
                        player.Avatar.add_star_tokens(1)
                        message.StarToken = True
                        player.Home.StarTokenReward += 1

                    hero.add_trophies(trophies_reward)

            if player.Avatar is None or player.GameListener is None:
                continue
            player.GameListener.send_tcp_message(message)

    def get_team_score(team: int) -> int:
        score = 0
        for player in self.game_players:
            if (player.team_index == team): score += player.get_score()
        return score

    def calculate_is_game_over(self) -> bool:
        ticks_gone = self.get_ticks_gone()

        if self.m_gameModeVariation == 3:
            if ticks_gone >= 20 * 120 + 120:
                if self.get_team_score(0) > self.get_team_score(1):
                    self.m_winnerTeam = 0
                elif self.get_team_score(0) < self.get_team_score(1):
                    self.m_winnerTeam = 1
                else:
                    self.m_winnerTeam = -1
                return True

        elif self.m_gameModeVariation == 0:
            team0_score = self.get_team_score(0)
            team1_score = self.get_team_score(1)

            if team0_score > team1_score and team0_score >= 10:
                if self.m_gemGrabCountdown == 0:
                    self.m_gemGrabCountdown = ticks_gone + 20 * 17
                elif ticks_gone > self.m_gemGrabCountdown:
                    self.m_winnerTeam = 0
                    return True

            elif team0_score < team1_score and team1_score >= 10:
                if self.m_gemGrabCountdown == 0:
                    self.m_gemGrabCountdown = ticks_gone + 20 * 17
                elif ticks_gone > self.m_gemGrabCountdown:
                    self.m_winnerTeam = 1
                    return True

            else:
                self.m_gemGrabCountdown = 0

        elif self.m_gameModeVariation == 6:
            if self.m_playersAlive <= 1:
                return True

        return False

    def tick():
        self.tick_spawn_event_stuff_delayed()
        self.game_object_manager.tick()
        self.tick_spawn_heroes()

    def send_vision_update(self):
        def update_player_vision(player):
            if player.GameListener is not None:
                vision_bit_stream = BitStream(64)
                self.m_gameObjectManager.encode(
                    vision_bit_stream, self.m_tileMap,
                    player.OwnObjectId, player.PlayerIndex, player.TeamIndex
                )

                vision_update = VisionUpdateMessage()
                vision_update.Tick = self.get_ticks_gone()
                vision_update.HandledInputs = player.LastHandledInput
                vision_update.Viewers = len(self.m_spectators)
                vision_update.VisionBitStream = vision_bit_stream

                player.GameListener.send_message(vision_update)

        # Parallel update for all players
        with ThreadPoolExecutor() as executor:
            executor.map(update_player_vision, self.m_players)

        # Prepare spectate stream
        spectate_stream = BitStream(64)
        self.m_gameObjectManager.encode(spectate_stream, self.m_tileMap, 0, -1, -1)

        # Send updates to spectators in a separate thread
        def update_spectators():
            for game_listener in list(self.m_spectators.values()):
                vision_update = VisionUpdateMessage()
                vision_update.Tick = self.get_ticks_gone()
                vision_update.HandledInputs = game_listener.HandledInputs
                vision_update.Viewers = len(self.m_spectators)
                vision_update.VisionBitStream = spectate_stream

                game_listener.send_message(vision_update)

        threading.Thread(target=update_spectators).start()

    def GetPlayers():
        return list(self.game_players.values())

    def get_random_int(a: int, b: int) -> int:
        return random.randrange(a, b)

    