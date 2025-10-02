from Logic.Battle.Structures.BattlePlayer import BattlePlayer
from Logic.Titan.Math import LogicVector2


class GameObject:
    def __init__(self, class_id: int, instance_id: int):
        self.data_id: int = GlobalId.create_global_id(class_id, instance_id)
        self.manager: "GameObjectManager" = None
        self.object_global_id: int = 0
        self.index: int = 0
        self.fade_counter: int = 10
        self.position: LogicVector2 = LogicVector2()
        self.z: int = 0

    # -------------------- Tick / Encoding --------------------
    def tick(self):
        pass

    def pre_tick(self):
        pass

    def encode(self, writer: "Writer", is_own_object: bool, vision_team: int):
        writer.write_vint(self.position.x)
        writer.write_vint(self.position.y)
        writer.write_vint(self.index)
        writer.write_vint(self.z)

    # -------------------- Visibility --------------------
    def set_forced_visible(self):
        self.fade_counter = 10

    def set_forced_invisible(self):
        self.fade_counter = 0

    def increment_fade_counter(self):
        if self.fade_counter < 10:
            self.fade_counter += 1

    def decrement_fade_counter(self):
        if self.fade_counter > 0:
            self.fade_counter -= 1

    def get_fade_counter(self) -> int:
        return self.fade_counter

    # -------------------- Position --------------------
    def set_position(self, x: int, y: int, z: int):
        self.position.set(x, y)
        self.z = z

    def get_position(self) -> LogicVector2:
        return self.position.clone()

    def get_x(self) -> int:
        return self.position.x

    def get_y(self) -> int:
        return self.position.y

    def get_z(self) -> int:
        return self.z

    # -------------------- Manager / Player --------------------
    def attach_game_object_manager(self, manager: "GameObjectManager", global_id: int):
        self.manager = manager
        self.object_global_id = global_id

    def get_player(self) -> BattlePlayer:
        return self.manager.get_battle().get_player(self.object_global_id)

    def get_global_id(self) -> int:
        return self.object_global_id

    def get_data_id(self) -> int:
        return self.data_id

    # -------------------- Index --------------------
    def set_index(self, i: int):
        self.index = i

    def get_index(self) -> int:
        return self.index

    # -------------------- Status --------------------
    def should_destruct(self) -> bool:
        return False

    def on_destruct(self):
        pass

    def is_alive(self) -> bool:
        return True

    # -------------------- Object Info --------------------
    def get_radius(self) -> int:
        return 100

    def get_size(self) -> int:
        return 100

    def get_object_type(self) -> int:
        return -1
