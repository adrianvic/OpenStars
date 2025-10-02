class GameModeUtils:
    @staticmethod
    def players_collect_power_cubes(variation: int) -> bool:
        v1 = variation - 6
        if v1 <= 8:
            return ((0x119 >> v1) & 1) != 0
        return False

    @staticmethod
    def get_respawn_seconds(variation: int) -> int:
        if variation in (0, 2):
            return 3
        elif variation == 3:
            return 1
        return 5

    @staticmethod
    def players_collect_bounty_stars(variation: int) -> bool:
        return variation in (3, 15)

    @staticmethod
    def has_two_teams(variation: int) -> bool:
        return variation != 6

    @staticmethod
    def get_game_mode_variation(mode: str) -> int:
        mapping = {
            "CoinRush": 0,
            "AttackDefend": 2,
            "BossFight": 7,
            "BountyHunter": 3,
            "Artifact": 4,
            "LaserBall": 5,
            "BattleRoyale": 6,
            "BattleRoyaleTeam": 9,
            "Survival": 8,
            "Raid": 10,
            "RoboWars": 11,
            "Tutorial": 12,
            "Training": 13,
        }
        return mapping.get(mode, -1)  # maybe log error if needed
