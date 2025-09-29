from ByteStream.Reader import Reader
from Logic.Home.LogicShopData import LogicShopData

class LogicPurchaseHeroLvlUpMaterialCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()
        self.gold_value = self.readVInt()


    def process(self, db):
        self.player.box_tokens += LogicShopData.gold_packs[self.gold_value]['Amount']
        self.player.gems -= LogicShopData.gold_packs[self.gold_value]['Cost']