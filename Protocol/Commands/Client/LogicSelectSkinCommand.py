from ByteStream.Reader import Reader
from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters

class LogicSelectSkinCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()
        self.skinID = self.readDataReference()[1]


    def process(self, db):
        self.player.home_brawler = Characters.get_brawler_by_skin_id(self, self.skinID)
        self.player.selected_skins[str(self.player.home_brawler)] = self.skinID
        self.player.starpower = Cards.get_spg_by_brawler_id(self, self.player.home_brawler, 4)
        self.player.gadget    = Cards.get_spg_by_brawler_id(self, self.player.home_brawler, 5)
