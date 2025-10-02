from Logic.Data.LogicData import LogicData
from Logic.Data.Row import Row

class SkillData(LogicData):
    def __init__(self, row: Row, data_table):
        super().__init__(row, data_table)
        self.load_data_from_row(row)

    def load_data_from_row(self, row: Row):
        """Load skill-specific fields from the CSV row"""
        # Strings
        self.name = row.get_value(0)
        self.behavior_type = row.get_value(1)
        self.projectile = row.get_value(2)
        self.summoned_character = row.get_value(3)
        self.area_effect_object = row.get_value(4)
        self.area_effect_object2 = row.get_value(5)
        self.spawned_item = row.get_value(6)
        self.icon_swf = row.get_value(7)
        self.icon_export_name = row.get_value(8)
        self.large_icon_swf = row.get_value(9)
        self.large_icon_export_name = row.get_value(10)
        self.button_swf = row.get_value(11)
        self.button_export_name = row.get_value(12)
        self.attack_effect = row.get_value(13)
        self.use_effect = row.get_value(14)
        self.end_effect = row.get_value(15)
        self.loop_effect = row.get_value(16)
        self.loop_effect2 = row.get_value(17)
        self.charge_move_sound = row.get_value(18)
        self.secondary_projectile = row.get_value(19)

        # Booleans
        self.can_move_at_same_time = row.get_bool(20)
        self.targeted = row.get_bool(21)
        self.can_auto_shoot = row.get_bool(22)
        self.face_movement = row.get_bool(23)
        self.two_guns = row.get_bool(24)
        self.execute_first_attack_immediately = row.get_bool(25)
        self.break_invisibility_on_attack = row.get_bool(26)
        self.always_cast_at_max_range = row.get_bool(27)
        self.multi_shot = row.get_bool(28)
        self.skill_can_change = row.get_bool(29)
        self.show_timer_bar = row.get_bool(30)

        # Integers
        self.cooldown = row.get_int(31)
        self.active_time = row.get_int(32)
        self.casting_time = row.get_int(33)
        self.casting_range = row.get_int(34)
        self.range_visual = row.get_int(35)
        self.range_input_scale = row.get_int(36)
        self.max_casting_range = row.get_int(37)
        self.force_valid_tile = row.get_int(38)
        self.recharge_time = row.get_int(39)
        self.max_charge = row.get_int(40)
        self.damage = row.get_int(41)
        self.ms_between_attacks = row.get_int(42)
        self.spread = row.get_int(43)
        self.attack_pattern = row.get_int(44)
        self.num_bullets_in_one_attack = row.get_int(45)
        self.charge_pushback = row.get_int(46)
        self.charge_speed = row.get_int(47)
        self.charge_type = row.get_int(48)
        self.num_spawns = row.get_int(49)
        self.max_spawns = row.get_int(50)
        self.see_invisibility_distance = row.get_int(51)
        self.charged_shot_count = row.get_int(52)
        self.damage_modifier = row.get_int(53)
