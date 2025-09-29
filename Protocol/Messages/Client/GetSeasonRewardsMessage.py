from ByteStream.Reader import Reader

class GetSeasonRewardsMessage(Reader):
    def __init__(self, client, player, data):
        super().__init__(data)
        self.client = client
        self.player = player

    def decode(self):
        pass

    def process(self, db):
        pass
