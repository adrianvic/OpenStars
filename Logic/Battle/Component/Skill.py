from LogicVector2 import LogicVector2
from DataTables import DataTables
from Utils.Writer import Writer
from Utils.Reader import Reader
from Utils.Math import LogicMath

class Skill:
    def __init__(self, global_id: int, is_ulti_skill: bool):
        self.skill_id = global_id
        self.is_ulti_skill = is_ulti_skill
        self.skill_data = DataTables.get_data_by_global_id(global_id)  # implement this method
        self.max_charge = max(1000, 1000 * self.skill_data.max_charge)
        self.charge = self.max_charge
        self.ticks_active = -1
        self.active_time = 0
        self.x = 0
        self.y = 0

        if self.skill_data.attack_pattern == 6:
            self.attack_pattern_table = [0] * 4
            p = 0
            sp = -(self.skill_data.spread // 6) * 2
            for i in range(4):
                if i >= 2:
                    self.attack_pattern_table[i] = sp if i == 2 else -sp
                else:
                    self.attack_pattern_table[i] = p
                    p += self.skill_data.spread // 6
        else:
            self.attack_pattern_table = []

    @property
    def is_active(self):
        return 0 <= self.ticks_active < self.active_time + 1

    @property
    def should_end_this_tick(self):
        return self.ticks_active >= self.active_time

    def has_enough_charge(self):
        return self.charge >= 1000

    def interrupt(self):
        self.ticks_active = -1

    def tick(self):
        if self.charge < self.max_charge and not self.is_active and self.skill_data.max_charge != 0:
            self.charge += 1000 // (self.skill_data.recharge_time // 50)
            self.charge = min(self.max_charge, self.charge)
        if self.is_active:
            self.ticks_active += 1

    def activate(self, character, x, y, tile_map):
        if self.charge < 1000 and self.skill_data.max_charge != 0:
            return

        self.charge -= 1000
        if self.is_ulti_skill:
            character.interrupt_all_skills()

        self.x = x
        self.y = y
        self.ticks_active = 1

        if self.skill_data.behavior_type != "Charge":
            self.active_time = (self.skill_data.active_time // 50) - 1
        else:
            self.active_time = self.skill_data.casting_range // 2

        character.block_health_regen()

    def should_attack_this_tick(self):
        if self.ticks_active == 0:
            return self.skill_data.execute_first_attack_immediately
        return self.ticks_active % (self.skill_data.ms_between_attacks // 50) == 0

    # Encode using Writer
    def encode(self, writer: Writer):
        writer.writePositiveVIntMax255OftenZero(self.ticks_active + 1 if self.is_active else 0)
        writer.writeBoolean(False)
        writer.writePositiveVIntMax255OftenZero(0)
        if self.skill_data.max_charge >= 1:
            writer.writePositiveIntMax4095(self.charge)
        if self.skill_data.skill_can_change:
            instance_id = self.skill_data.get_instance_id()
            writer.writePositiveIntMax255(instance_id)

    def get_skill_range_add_from_hold(self, ticks: int):
        if self.skill_data.attack_pattern != 13:
            return 0
        return min(ticks // 2, 120)  # assuming Character.MAX_SKILL_HOLD_TICKS = 240

    def get_max_charge(self):
        return self.max_charge

    def has_button(self):
        return True

    def is_ok_to_reduce_cooldown(self):
        return True

    def max_cooldown(self):
        return self.skill_data.cooldown
