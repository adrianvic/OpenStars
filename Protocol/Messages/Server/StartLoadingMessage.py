from Protocol.Messages.GameMessage import GameMessage
from Logic.Battle.Structures.BattlePlayer import BattlePlayer
from ByteStream import Writer
from Utils.ByteStreamHelper import write_data_reference

class StartLoadingMessage(GameMessage):
    def __init__(self, client=None):
        super().__init__(client)
        self.players: list[BattlePlayer] = []
        self.own_index: int = 0
        self.team_index: int = 0
        self.location_id: int = 0
        self.game_mode: int = 0
        self.spectate_mode: int = 0

    def encode(self):
        w: Writer = self.writer

        # Basic info
        w.writeInt(len(self.players))
        w.writeInt(self.own_index)
        w.writeInt(self.team_index)

        # Players array
        w.writeInt(len(self.players))
        for player in self.players:
            player.encode(w)

        # Empty arrays
        w.writeInt(0)
        w.writeInt(0)

        # Random seed
        w.writeInt(0)

        # Game settings
        w.writeVInt(self.game_mode)
        w.writeVInt(1)
        w.writeVInt(1)
        w.writeBool(True)
        w.writeVInt(self.spectate_mode)
        w.writeVInt(0)
        write_data_reference(w, self.location_id)
        w.writeBool(False)

    def get_message_type(self) -> int:
        return 20559

    def get_service_node_type(self) -> int:
        return 4
