from ByteStream.Reader import Reader
from ByteStream.Writer import Writer

class ClientCapabilitiesMessage(Reader, Writer):
    def __init__(self, client, player, data=None):
        if data is None:
            Writer.__init__(self, client)
        else:
            Reader.__init__(self, data)
        self.client = client
        self.player = player
        self.ping = 0

    def decode(self):
        self.ping = self.readVInt()

    def encode(self):
        self.writeVInt(self.ping) # placeholder

    def process(self, db):
        pass
