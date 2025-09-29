from ByteStream.Reader import Reader

class ChronosEventSeenMessage(Reader):
    def __init__(self, client, player, data):
        super().__init__(data)
        self.client = client
        self.player = player
        self.unknown = 0

    def decode(self):
        self.unknown = self.readVInt()

    def process(self, db):
        pass
