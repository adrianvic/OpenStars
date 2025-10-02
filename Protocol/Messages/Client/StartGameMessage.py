import random
from Logic.Battle.BattleMode import BattleMode
from Logic.Battle.Structures.BattlePlayer import BattlePlayer
from Logic.Home.LogicEventData import LogicEventData
from Protocol.Messages.Server.StartLoadingMessage import StartLoadingMessage
from Protocol.Messages.Server.TeamMessage import TeamMessage
from Protocol.Messages.Server.MatchMakingCancelledMessage import MatchMakingCancelledMessage

bot_brawlers = [0, 1, 2, 3, 9, 18]  # allowed bot IDs

class MatchmakingSlot:
    def __init__(self, event_data, players_required):
        self.event_data = event_data
        self.players_required = players_required
        self.queue = []

    def add(self, entry):
        self.queue.append(entry)

    def start_game(self):
        if not self.queue:
            return

        battle = BattleMode(self.event_data.get("LocationID"))
        battle_id = id(battle)  # simple battle ID placeholder

        sorted_entries = self.queue.copy()
        self.queue.clear()

        # assign BattlePlayers to human clients
        for i, entry in enumerate(sorted_entries):
            team_index = i % 2 if self.event_data.get("Teams", 2) == 2 else i
            player = BattlePlayer(entry.player.ID, team_index, entry.player)
            player.team_id = entry.PlayerTeamId
            entry.Player = player
            battle.add_player(player, entry.player.ID)  # ID as session placeholder

        # fill remaining slots with dummy bots
        for i in range(len(sorted_entries), self.players_required):
            team_index = i % 2 if self.event_data.get("Teams", 2) == 2 else i
            bot_char = 16000000 + random.choice(bot_brawlers)
            bot_name = f"BOT_{bot_char}"
            bot = BattlePlayer(i, team_index, is_bot=True, name=bot_name, character=bot_char)
            battle.add_player(bot, -1)

        # send messages to clients so they see the battle
        for entry in sorted_entries:
            start_msg = StartLoadingMessage(entry.player)
            start_msg.location_id = battle.location.get("LocationID", 0)
            start_msg.team_index = entry.Player.team_index
            start_msg.own_index = entry.Player.player_index
            start_msg.players = battle.get_players()
            start_msg.send(entry.player)

            TeamMessage(entry.player).send()
            MatchMakingCancelledMessage(entry.player).send()

        battle.start()  # start battle locally (no AI/movement required)
