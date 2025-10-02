from collections import deque
from typing import List, Optional

from Logic.Battle.Level.TileMap import TileMap
from Logic.Battle.Structures.BattlePlayer import BattlePlayer
from Logic.Battle.Objects.GameObject import GameObject
from Logic.Battle.Objects.GlobalId import GlobalId
from Logic.Helper.ByteStreamHelper import ByteStreamHelper


class GameObjectManager:
    def __init__(self, battle: "BattleMode"):
        self.battle = battle
        self.game_objects: List[GameObject] = []
        self.add_objects: deque[GameObject] = deque()
        self.remove_objects: deque[GameObject] = deque()
        self.object_counter: int = 0

    # -------------------- Accessors --------------------
    def get_game_objects(self) -> List[GameObject]:
        return list(self.game_objects)

    def get_object_by_id(self, global_id: int) -> Optional[GameObject]:
        for obj in self.game_objects:
            if obj.get_global_id() == global_id:
                return obj
        return None

    def get_visible_game_objects(self, team_index: int) -> List[GameObject]:
        return [
            obj for obj in self.game_objects
            if obj.get_fade_counter() > 0 or obj.get_index() // 16 == team_index
        ]

    def get_battle(self) -> "BattleMode":
        return self.battle

    # -------------------- Tick Management --------------------
    def pre_tick(self):
        """Handle destruction and pre-tick for all objects"""
        for obj in list(self.game_objects):
            if obj.should_destruct():
                obj.on_destruct()
                self.remove_game_object(obj)
            else:
                obj.pre_tick()

        while self.add_objects:
            self.game_objects.append(self.add_objects.popleft())

        while self.remove_objects:
            obj = self.remove_objects.popleft()
            if obj in self.game_objects:
                self.game_objects.remove(obj)

    def tick(self):
        """Call tick on all game objects"""
        for obj in self.game_objects:
            obj.tick()

    # -------------------- GameObject Management --------------------
    def add_game_object(self, obj: GameObject):
        """Attach object to manager and assign a global ID"""
        global_id = GlobalId.create_global_id(obj.get_object_type(), self.object_counter)
        self.object_counter += 1
        obj.attach_game_object_manager(self, global_id)
        self.add_objects.append(obj)

    def remove_game_object(self, obj: GameObject):
        self.remove_objects.append(obj)

    # -------------------- Protocol Encoding --------------------
    def encode(self, writer, tile_map: TileMap, own_object_global_id: int, player_index: int, team_index: int):
        battle = self.battle
        players = battle.get_players()
        visible_objects = self.get_visible_game_objects(team_index)
        game_mode_variation = battle.game_mode_variation

        writer.write_vint(own_object_global_id)

        if game_mode_variation == 0:  # Gem Grab
            writer.write_vint(battle.get_gem_grab_countdown())

        writer.write_boolean(False)
        writer.write_vint(-1)
        writer.write_boolean(True)
        writer.write_boolean(True)
        writer.write_boolean(True)
        writer.write_boolean(False)

        writer.write_vint(0)
        writer.write_vint(0)
        writer.write_vint(tile_map.width - 1)
        writer.write_vint(tile_map.height - 1)

        for i in range(tile_map.width):
            for j in range(tile_map.height):
                tile = tile_map.get_tile(i, j, True)
                if tile.data.respawn_seconds > 0 or tile.data.is_destructible:
                    writer.write_boolean(tile.is_destructed())

        writer.write_vint(1)
        for i, player in enumerate(players):
            writer.write_vint(0)
            writer.write_boolean(player.has_ulti())
            if game_mode_variation == 6:
                writer.write_vint(0)
            if i == player_index:
                writer.write_vint(player.get_ulti_charge())
                writer.write_vint(0)
                writer.write_vint(0)

        writer.write_vint(1)
        if game_mode_variation == 6:
            writer.write_vint(battle.get_players_alive_battle_royale())

        for player in players:
            if game_mode_variation != 6:
                writer.write_boolean(True)
                writer.write_vint(player.get_score())
            else:
                writer.write_boolean(False)

            if len(player.kill_list) > 0:
                writer.write_boolean(True)
                writer.write_vint(len(player.kill_list))
                for kill in player.kill_list:
                    writer.write_vint(kill.player_index)
                    writer.write_vint(kill.bounty_stars_earned)
            else:
                writer.write_boolean(False)

        writer.write_vint(len(visible_objects))
        for obj in visible_objects:
            ByteStreamHelper.write_data_reference(writer, obj.get_data_id())

        for obj in visible_objects:
            writer.write_vint(GlobalId.get_instance_id(obj.get_global_id()))

        for obj in visible_objects:
            obj.encode(writer, obj.get_global_id() == own_object_global_id, team_index)

        writer.write_vint(0)
