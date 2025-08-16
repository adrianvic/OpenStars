from Utils.Logger import Logger

class PlayerTransactions:
    @staticmethod
    def coins(player, amount):
        player.resources[1]['Amount'] += amount
        player.db.update_player_account(player.token, 'Resources', player.resources)
        Logger.log("TRANSACTION", f'[{player.name}] Coins ({amount}) successful')

    @staticmethod
    def gems(player, amount):
        player.gems += amount
        player.db.update_player_account(player.token, 'Gems', player.gems)
        Logger.log("TRANSACTION", f'[{player.name}] Gems ({amount}) successful')

    @staticmethod
    def token_doubler(player, amount):
        player.token_doubler += amount
        player.db.update_player_account(player.token, 'TokenDoubler', player.token_doubler)
        Logger.log("TRANSACTION", f'[{player.name}] Token Doubler ({amount}) successful')

    @staticmethod
    def power_points(player, brawler, amount, levelCap = 9):
        brawler_level = int(player.brawlers_level[brawler])
        if brawler_level >= levelCap and levelCap >= 0:
            Logger.log("TRANSACTION", f'[{player.name}] PP Transaction ({brawler} {amount}) was capped because {brawler_level} > {levelCap}')
            return False
        player.brawlers_powerpoints[brawler] += amount
        player.db.update_player_account(player.token, 'BrawlersPowerPoints', player.brawlers_powerpoints)
        Logger.log("TRANSACTION", f'[{player.name}] PP Transaction ({brawler} {amount}) successful')
        return True

    @staticmethod
    def give_brawler(player, brawler):
        if brawler not in player.brawlers_unlocked:
            player.brawlers_unlocked.append(brawler)
            player.db.update_player_account(player.token, 'UnlockedBrawlers', player.brawlers_unlocked)
            Logger.log('transaction', f'[{player.name}] Brawler unlocked: {brawler}')
            return True
        Logger.log('transaction', f'[{player.name}] Brawler NOT unlocked: {brawler}')
        return False