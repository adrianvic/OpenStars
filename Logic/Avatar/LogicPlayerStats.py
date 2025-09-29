class LogicPlayerStats:

    def getPlayerStats(self):

        accountData = self.player_data
        
        playerStats = {
            '3v3Victories': 0,
            'ExperiencePoints': accountData.experience_points,
            'Trophies': accountData.trophies,
            'HighestTrophies': accountData.highest_trophies,
            'UnlockedBrawlersCount': len(accountData.brawlers_unlocked),
            'Unknown2': 0,
            'ProfileIconID': 28000000 + accountData.profile_icon,
            'SoloVictories': 0,
            'BestRoboRumbleTime': 9999,
            'BestTimeAsBigBrawler': 99999,
            'DuoVictories': 0,
            'HighestBossFightLvlPassed': 21,
            'Unknown4': 0,
            'PowerPlayRank': 1,
            'MostChallengeWins': 0
        }

        return playerStats