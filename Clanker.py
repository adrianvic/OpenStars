from Logic.Player import Player
from Utils.Helpers import Helpers
from Utils.Logger import Logger

class Clanker:
    _active_players: dict[str, Player] = {}

    @classmethod
    def get_or_create(cls, player_id, db):
        # Return existing instance if available
        if player_id in cls._active_players:
            return cls._active_players[player_id]

        # Load from DB
        data = db.load_player_account_by_id(player_id)

        if data is None:
            return None

        # Create Player instance and load data
        player = Player(player_id, db)
        player.load_from_data(data)

        # Auto-add to memory
        cls._active_players[player_id] = player

        return player

    @classmethod
    def insert_preloaded(cls, player):
        cls._active_players[player.ID] = player

    @classmethod
    def remove(cls, player_id):
        if player_id in cls._active_players:
            cls._active_players.pop(player_id)
            Helpers.connected_clients['ClientsCount'] = max(
                0, Helpers.connected_clients.get('ClientsCount', 1) - 1
            )

    @classmethod
    def get(cls, player_id):
        return cls._active_players.get(player_id)
