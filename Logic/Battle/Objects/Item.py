class Item(GameObject):
    def __init__(self, class_id, instance_id):
        super().__init__(class_id, instance_id)
        self._picked_up = False
        self._should_play_appear_animation = True
        self._angle = 0
        self._ticks_gone = 0
        self._picker = None
        self._ticks_since_pick_up = 0

    @property
    def item_data(self):
        return DataTables.get(DataType.Item).get_data_by_global_id(self.data_id)

    def tick(self):
        self._ticks_gone += 1

        if self.item_data.can_be_picked_up and self._should_play_appear_animation:
            if self._ticks_gone <= 10:
                dx = LogicMath.cos(self._angle) // 20
                dy = LogicMath.sin(self._angle) // 20

                new_x = self.get_x() + dx
                new_y = self.get_y() + dy

                tx = TileMap.logic_to_tile(new_x)
                ty = TileMap.logic_to_tile(new_y)

                tile_map = GameObjectManager.get_battle().get_tile_map()

                if 0 < tx < tile_map.width:
                    self.position.x = new_x
                if 0 < ty < tile_map.height:
                    self.position.y = new_y

                if self._ticks_gone <= 5:
                    self.z += 120
                else:
                    self.z -= 120

            elif self._ticks_gone <= 14:
                v1 = self._ticks_gone - 10
                if v1 <= 2:
                    self.z += 120 // v1
                else:
                    self.z -= 120 // (v1 - 2)

        if self._picked_up:
            self._ticks_since_pick_up += 1
            angle_rad = self._angle - (3.14159265 * 90 / 180)
            delta_x = int(0.05 * LogicMath.cos(int(angle_rad)))
            delta_y = int(0.05 * LogicMath.sin(int(angle_rad)))

            self.position.x += delta_x
            self.position.y += delta_y
            self.z += 120

            if self._ticks_since_pick_up >= 4:
                self._picker.apply_item(self)
                GameObjectManager.remove_game_object(self)

    def pick_up(self, character):
        self._should_play_appear_animation = False
        self._picked_up = True
        self._picker = character
        self._ticks_since_pick_up = 0

        dx = character.get_x() - self.position.x
        dy = character.get_y() - self.position.y
        self._angle = LogicMath.get_angle(dx, dy)

    def set_angle(self, angle):
        self._angle = angle

    def disable_appear_animation(self):
        self._should_play_appear_animation = False

    def can_be_picked_up(self):
        return self.item_data.can_be_picked_up and not self._picked_up

    def encode(self, bit_stream, is_own_object, vision_team):
        super().encode(bit_stream, is_own_object, vision_team)
        bit_stream.write_positive_int(10, 4)

        if self.item_data.name == "OrbSpawner":
            bit_stream.write_positive_int_max16383(0)
            bit_stream.write_positive_int_max16383(0)

    def get_object_type(self):
        return 4
