from Utils.Logger import Logger

class PlayerTransactions:
    @staticmethod
    def coins(player, amount):
        player.coins += amount
        Logger.log("TRANSACTION", f'[{player.name}] Coins ({amount}) successful')

    @staticmethod
    def gems(player, amount):
        player.gems += amount
        Logger.log("TRANSACTION", f'[{player.name}] Gems ({amount}) successful')

    @staticmethod
    def token_doubler(player, amount):
        player.token_doubler += amount
        Logger.log("TRANSACTION", f'[{player.name}] Token Doubler ({amount}) successful')

    @staticmethod
    def power_points(player, brawler, amount, levelCap = 9):
        brawler_level = int(player.brawlers_level[brawler])
        if brawler_level >= levelCap and levelCap >= 0:
            Logger.log("TRANSACTION", f'[{player.name}] PP Transaction ({brawler} {amount}) was capped because {brawler_level} > {levelCap}')
            return False
        player.brawlers_power_points[brawler] += amount
        Logger.log("TRANSACTION", f'[{player.name}] PP Transaction ({brawler} {amount}) successful')
        return True

    @staticmethod
    def brawler(player, brawler):
        if brawler not in player.brawlers_unlocked:
            player.brawlers_unlocked.append(brawler)
            Logger.log('transaction', f'[{player.name}] Brawler unlocked: {brawler}')
            return True
        Logger.log('transaction', f'[{player.name}] Brawler NOT unlocked: {brawler}')
        return False

    @staticmethod
    def remove_brawer(player, brawler, verbose = True):
        if brawler in player.brawlers_unlocked:
            player.brawlers.remove(brawler)
            if verbose: Logger.log('transaction', f'[{player.name}] Brawler removed: {brawler}')

    @staticmethod
    def trophies(player, amount, brawler):
        player.brawlers_trophies[str(brawler)] += amount
        PlayerTransactions.reload_trophies(player)
        Logger.log("TRANSACTION", f'[{player.name}] Won {amount} trophies for brawler {brawler} ({player.brawlers_trophies[str(brawler)]})')

    @staticmethod
    def reload_trophies(player):
        total = 0
        for brawler in player.brawlers_trophies:
            total += player.brawlers_trophies[brawler]
        player.trophies = total
        return total