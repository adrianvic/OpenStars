from ByteStream.Reader import Reader

class TeamMemberStatusMessage(Reader):
    def __init__(self, client, player, data):
        super().__init__(data)
        self.client = client
        self.player = player
        self.status = 0

    def decode(self):
        self.status = self.readVInt()

    def process(self, db):
        pass
