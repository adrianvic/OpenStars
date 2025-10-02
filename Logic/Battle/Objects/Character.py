class Character(GameObject):
    MAX_SKILL_HOLD_TICKS = 15
    INTRO_TICKS = 120

    def __init__(self, class_id, instance_id, battle):
        super().__init__(class_id, instance_id)
        self.battle = battle
        self.m_hitpoints = 0
        self.m_max_hitpoints = 0
        self.m_state = 4
        self.m_angle = 0
        self.m_is_moving = False
        self.m_using_ulti_currently = False
        self.m_movement_destination = None
        self.m_tick_when_health_regen_blocked = 0
        self.m_last_self_heal_tick = 0
        self.m_holding_skill = False
        self.m_skill_hold_ticks_gone = 0
        self.m_skills = []
        self.m_item_count = 0
        self.m_hero_level = 0
        self.m_is_bot = False
        self.m_ticks_since_bot_enemy_check = 100
        self.m_last_ai_attack_tick = 0
        self.m_closest_enemy = None
        self.m_closest_enemy_position = None
        self.m_active_charge_type = -1
        self.m_is_stunned = False
        self.m_ticks_gone_since_stunned = 0
        self.m_damage_multiplier = 0
        self.m_last_tile_damage_tick = 0
        self.m_damage_indicator = []
        self.m_immunity = None
        self.m_attacking_ticks = 0
        self.m_poison = None

        # Melee attack
        self.m_melee_attack_end_tick = -1
        self.m_melee_attack_target = None
        self.m_melee_attack_damage = 0

        # Charge skill
        self.jump_charge_destination = None
        self.charge_time = 0
        self.spread_index = 0

        # Shaman pet target
        self.shaman_pet_target = None

        # Initialize character stats
        self.m_max_hitpoints = self.character_data.hitpoints
        self.m_hitpoints = self.m_max_hitpoints

        if self.weapon_skill_data:
            self.m_skills.append(Skill(self.weapon_skill_data.global_id, False))
        if self.ultimate_skill_data:
            self.m_skills.append(Skill(self.ultimate_skill_data.global_id, True))

    # -------------------- Properties --------------------
    @property
    def character_data(self):
        return DataTables.get(DataType.Character).get_data_by_global_id(self.data_id)

    @property
    def weapon_skill_data(self):
        return DataTables.get(DataType.Skill).get_data(self.character_data.weapon_skill)

    @property
    def ultimate_skill_data(self):
        return DataTables.get(DataType.Skill).get_data(self.character_data.ultimate_skill)

    # -------------------- Tick / AI --------------------
    def pre_tick(self):
        self.m_damage_indicator.clear()

    def tick(self):
        self.handle_move_and_attack()

        if self.m_holding_skill:
            self.m_skill_hold_ticks_gone += 1

        for skill in self.m_skills:
            skill.tick()

        if self.battle.get_battle().get_ticks_gone() > self.INTRO_TICKS:
            self.tick_timers()

        self.tick_tile()

        if self.character_data.is_hero():
            self.tick_heals()

        if self.m_attacking_ticks < 63:
            self.m_attacking_ticks += 1

        if self.battle.get_battle().get_ticks_gone() > self.INTRO_TICKS:
            self.tick_ai()

    def tick_timers(self):
        if self.m_immunity and self.m_immunity.tick(1):
            self.m_immunity.destruct()
            self.m_immunity = None

        if self.m_poison and self.m_poison.tick(self):
            self.m_poison.destruct()
            self.m_poison = None

    def tick_tile(self):
        tile_map = self.battle.get_battle().get_tile_map()
        tile = tile_map.get_tile(self.get_x(), self.get_y())
        if tile.data.hides_hero and not tile.is_destructed():
            self.decrement_fade_counter()
        else:
            self.increment_fade_counter()

        x = TileMap.logic_to_tile(self.get_x())
        y = TileMap.logic_to_tile(self.get_y())
        if self.battle.get_battle().get_ticks_gone() - self.m_last_tile_damage_tick > 20:
            if self.battle.get_battle().is_tile_on_poison_area(x, y):
                self.m_last_tile_damage_tick = self.battle.get_battle().get_ticks_gone()
                self.cause_damage(None, 1000)

    # -------------------- Movement --------------------
    def stop_movement(self):
        self.m_is_moving = False

    def move_to(self, x, y):
        if not self.battle.get_battle().is_in_play_area(x, y):
            return
        if self.is_charge_active():
            return
        self.m_is_moving = True
        if self.m_attacking_ticks >= 63:
            self.m_state = 1
        self.m_movement_destination = LogicVector2(x, y)
        delta = self.m_movement_destination.clone()
        delta.substract(self.position)
        if not (-150 < delta.x < 150 and -150 < delta.y < 150):
            self.m_angle = LogicMath.get_angle(delta.x, delta.y)

    def check_obstacle(self, next_tiles):
        moving_speed = self.character_data.speed // 20
        new_x, new_y = self.position.x, self.position.y

        for _ in range(next_tiles):
            delta_x = min(moving_speed, self.m_movement_destination.x - self.position.x) if self.m_movement_destination.x - self.position.x > 0 else max(-moving_speed, self.m_movement_destination.x - self.position.x)
            delta_y = min(moving_speed, self.m_movement_destination.y - self.position.y) if self.m_movement_destination.y - self.position.y > 0 else max(-moving_speed, self.m_movement_destination.y - self.position.y)
            new_x += delta_x
            new_y += delta_y
            if not self.battle.get_battle().is_in_play_area(new_x, new_y):
                return True
            next_tile = self.battle.get_battle().get_tile_map().get_tile(new_x, new_y)
            if not next_tile or (next_tile.data.blocks_movement and not next_tile.is_destructed()):
                return True
        return False

    def handle_move_and_attack(self):
        if not self.has_active_skill():
            self.m_attacking_ticks = 63

        if self.m_is_stunned:
            self.m_ticks_gone_since_stunned += 1
            if self.m_ticks_gone_since_stunned > 40:
                self.m_is_stunned = False
            return

        # Interact with nearby objects
        for obj in self.battle.get_game_objects():
            if self.position.get_distance(obj.get_position()) <= 200 and obj.get_index() // 16 != self.get_index() // 16:
                obj.set_forced_visible()
            if self.character_data.is_hero() and obj.get_object_type() == 4:
                if self.position.get_distance(obj.get_position()) < 350 and obj.can_be_picked_up():
                    obj.pick_up(self)

        # Melee attack
        if self.m_melee_attack_end_tick == self.battle.get_battle().get_ticks_gone():
            if self.m_melee_attack_target:
                self.m_melee_attack_target.cause_damage(None, self.m_melee_attack_damage)

        # Skill attacks
        for skill in self.m_skills:
            if not skill.is_active:
                continue
            if skill.skill_data.behavior_type == "Attack":
                if not skill.should_attack_this_tick():
                    continue
                projectile_data = DataTables.get(DataType.Projectile).get_data(skill.skill_data.projectile)
                damage = skill.skill_data.damage
                spread = skill.skill_data.spread
                bullets = skill.skill_data.num_bullets_in_one_attack
                self.attack(skill.x, skill.y, skill.skill_data.casting_range, projectile_data, damage, spread, bullets, skill)
            elif skill.skill_data.behavior_type == "Charge":
                self.m_active_charge_type = skill.skill_data.charge_type
                dx = LogicMath.cos(self.m_angle) // 100 * skill.skill_data.charge_speed // 80
                dy = LogicMath.sin(self.m_angle) // 100 * skill.skill_data.charge_speed // 80
                if not self.battle.get_battle().is_in_play_area(self.position.x + dx, self.position.y + dy):
                    skill.interrupt()
                    self.m_active_charge_type = -1
                    return
                tile = self.battle.get_battle().get_tile_map().get_tile(self.position.x + dx, self.position.y + dy)
                if not tile:
                    skill.interrupt()
                    self.m_active_charge_type = -1
                    return
                if tile.data.blocks_movement and not tile.is_destructed():
                    if tile.data.is_destructible:
                        tile.destruct()
                    else:
                        skill.interrupt()
                        self.m_active_charge_type = -1
                        return
                self.position.x += dx
                self.position.y += dy
                if skill.should_end_this_tick:
                    self.m_active_charge_type = -1

        # Movement
        if self.m_is_moving and not self.is_charge_active():
            if self.position.get_distance(self.m_movement_destination) != 0:
                angle = self.m_angle
                initial_dest_x = self.m_movement_destination.x
                initial_dest_y = self.m_movement_destination.y
                if self.m_is_bot or not self.character_data.is_hero():
                    while self.check_obstacle(15):
                        self.m_movement_destination.x = self.position.x
                        self.m_movement_destination.y = self.position.y
                        angle += 2
                        self.m_movement_destination.x += LogicMath.cos(angle)
                        self.m_movement_destination.y += LogicMath.sin(angle)
                else:
                    if self.check_obstacle(1):
                        self.stop_movement()
                self.m_angle = LogicMath.normalize_angle360(angle)
                moving_speed = self.character_data.speed // 20
                delta_x = min(moving_speed, self.m_movement_destination.x - self.position.x) if self.m_movement_destination.x - self.position.x > 0 else max(-moving_speed, self.m_movement_destination.x - self.position.x)
                delta_y = min(moving_speed, self.m_movement_destination.y - self.position.y) if self.m_movement_destination.y - self.position.y > 0 else max(-moving_speed, self.m_movement_destination.y - self.position.y)
                self.position.x += delta_x
                self.position.y += delta_y
            self.m_is_moving = self.position.get_distance(self.m_movement_destination) != 0
            if not self.m_is_moving:
                self.m_state = 4

    # -------------------- Skills --------------------
    def hold_skill_started(self):
        if not self.m_holding_skill:
            self.m_holding_skill = True
            self.m_skill_hold_ticks_gone = 0

    def skill_released(self):
        self.m_holding_skill = False

    def get_weapon_skill(self):
        return self.m_skills[0] if len(self.m_skills) > 0 else None

    def get_ultimate_skill(self):
        return self.m_skills[1] if len(self.m_skills) > 1 else None

    def has_active_skill(self):
        if len(self.m_skills) == 0:
            return False
        if len(self.m_skills) == 1:
            return self.m_skills[0].is_active
        return self.m_skills[0].is_active or self.m_skills[1].is_active

    def interrupt_all_skills(self):
        for skill in self.m_skills:
            skill.interrupt()

    def block_health_regen(self):
        self.m_tick_when_health_regen_blocked = self.battle.get_battle().get_ticks_gone()

    # -------------------- Damage --------------------
    def cause_damage(self, dealer, damage, show=True):
        try:
            if self.m_hitpoints <= 0:
                return
            if self.m_immunity:
                damage -= int(self.m_immunity.get_immunity_percentage() / 100 * damage)
            self.m_hitpoints = max(0, min(self.m_hitpoints - damage, self.m_max_hitpoints))
            if damage > 0:
                self.block_health_regen()
            if show:
                self.m_damage_indicator.append(damage)
            # ... handle players, loot, battle rules (omitted for brevity, copy logic from C#)
        except Exception:
            pass

    # -------------------- Other Methods --------------------
    def is_charge_active(self):
        return self.m_active_charge_type >= 0

    def get_hitpoint_percentage(self):
        return int((self.m_hitpoints / self.m_max_hitpoints) * 100)

    def is_alive(self):
        return self.m_hitpoints > 0

    def get_radius(self):
        return self.character_data.collision_radius

    def set_hero_level(self, level):
        self.m_hero_level = level
        self.m_max_hitpoints = self.character_data.hitpoints + int(0.05 * self.character_data.hitpoints) * level
        self.m_hitpoints = self.m_max_hitpoints
        self.m_damage_multiplier = level

    def get_hero_level(self):
        return self.m_hero_level

    def get_absolute_damage(self, damage):
        return damage + int(0.05 * damage) * (self.m_hero_level + self.m_damage_multiplier)