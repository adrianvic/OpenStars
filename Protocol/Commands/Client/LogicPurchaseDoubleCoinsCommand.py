from ByteStream.Reader import Reader
from Logic.Home.LogicShopData import LogicShopData

class LogicPurchaseDoubleCoinsCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()

    def process(self, db):
        self.player.token_doubler = self.player.token_doubler + LogicShopData.token_doubler[0]['Amount']
        self.player.gems = self.player.gems - LogicShopData.token_doubler[0]['Cost']