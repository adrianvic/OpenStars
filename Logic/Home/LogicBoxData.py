import random
from Logic.PlayerTransactions import PlayerTransactions

class LogicBoxData:
    REWARD_TYPE_10 = 10
    REWARD_TYPE_11 = 11
    REWARD_TYPE_12 = 12
    MAX_BRAWLER_LEVEL = 9

    def __init__(self, player):
        self.player = player
        self.box_rewards = {'Rewards': []}

    def randomize(self, type):
        self.box_rewards = {'Rewards': []}
        seed = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]

        if type == 10:
            if seed[0] < 20:
                self.generate_brawler_reward()
            self.generate_gold_reward(20, 100)
            self.generate_power_points_reward([1], 5, 30)
            self.generate_power_points_reward([1], 5, 20)
            self.generate_power_points_reward([1], 5, 10)
            self.generate_power_points_reward([1], 5, 5)

            if seed[1] < 1:
                self.generate_brawler_reward()

            if seed[2] < 30:
                self.generate_bonus_reward()
            if seed[1] < 90:
                self.generate_bonus_reward()

        elif type == 12:
            self.generate_gold_reward(60, 300)
            self.generate_power_points_reward([1], 15, 90)
            self.generate_power_points_reward([1], 15, 60)
            self.generate_power_points_reward([1], 15, 30)
            self.generate_power_points_reward([1], 15, 15)

            if seed[0] < 5:
                self.generate_brawler_reward()
            if seed[1] < 40:
                self.generate_bonus_reward()
            if seed[1] < 70:
                self.generate_bonus_reward()
            if seed[1] < 90:
                self.generate_bonus_reward()

        elif type == 11:
            self.generate_gold_reward(200, 1000)
            self.generate_power_points_reward([1], 50, 300)
            self.generate_power_points_reward([1], 50, 200)
            self.generate_power_points_reward([1], 50, 100)
            self.generate_power_points_reward([1], 50, 50)

            if seed[0] < 15:
                self.generate_brawler_reward()
            if seed[1] < 50:
                self.generate_bonus_reward()
            if seed[1] < 60:
                self.generate_bonus_reward()
            if seed[1] < 90:
                self.generate_bonus_reward()

        return self.box_rewards

    def generate_gold_reward(self, min_value, max_value):
        gold_value = random.randint(min_value, max_value)
        gold_reward = {'Amount': gold_value, 'DataRef': [0, 0], 'Value': 7}
        self.box_rewards['Rewards'].append(gold_reward)
        PlayerTransactions.coins(self.player, gold_value)
        

    def generate_brawler_reward(self):
        locked_brawlers = sorted(set(self.player.brawlers_id) - set(self.player.brawlers_unlocked))
        brawler = random.choice(self.player.brawlers_id)
        if PlayerTransactions.brawler(self.player, brawler):
            brawler_reward = {'Amount': 1, 'DataRef': [16, brawler], 'Value': 1}
            self.box_rewards['Rewards'].append(brawler_reward)

    def generate_power_points_reward(self, pp_range, pp_min, pp_max):
        rewarded = []
        for _ in range(random.choice(pp_range)):
            brawler = random.choice(sorted(set(self.player.brawlers_unlocked) - set(rewarded)))
            pp_value = random.randint(pp_min, pp_max)
            if PlayerTransactions.power_points(self.player, str(brawler), pp_value):
                pp_reward = {'Amount': pp_value, 'DataRef': [16, brawler], 'Value': 6}
                self.box_rewards['Rewards'].append(pp_reward)
                rewarded.append(brawler)

    def generate_bonus_reward(self):
        bonus_type = random.choice([2, 8])
        if bonus_type == 8:
            bonus_value = random.randint(1, 10)
            PlayerTransactions.gems(self.player, bonus_value)
        else:
            bonus_value = random.randint(20, 80)
            PlayerTransactions.token_doubler(self.player, bonus_value)
        bonus_reward = {'Amount': bonus_value, 'DataRef': [0, 0], 'Value': bonus_type}
        self.box_rewards['Rewards'].append(bonus_reward)