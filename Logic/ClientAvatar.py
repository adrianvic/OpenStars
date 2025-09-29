from ByteStream.Writer import Writer
from Files.CsvLogic.Cards import Cards
from Utils.Logger import Logger

class LogicClientAvatar:

    @staticmethod
    def encode(self: Writer):
        self.writeVInt(0)
        self.writeVInt(0)

        for x in range(3):
            self.writeLogicLong(self.player.ID)

        self.writeString(self.player.name)
        self.writeBoolean(self.player.name_set)

        self.writeInt(0)

        self.writeVInt(8) # Commodity Array

        # Unlocked Brawlers & Resources array
        self.writeVInt(len(self.player.get_resources()) + len(self.player.brawlers_card_id))

        for x in self.player.brawlers_card_id:
            self.writeDataReference(23, x)
            self.writeVInt(1)

        for resource in self.player.get_resources():
            self.writeDataReference(5, resource['ID'])
            self.writeVInt(resource['Amount'])

        self.writeVInt(len(self.player.brawlers_id))
        for x in self.player.brawlers_id:
            self.writeDataReference(16, x)
            self.writeVInt(self.player.brawlers_trophies[str(x)])

        self.writeVInt(len(self.player.brawlers_id))
        for x in self.player.brawlers_id:
            self.writeDataReference(16, x)
            self.writeVInt(self.player.brawlers_highest_trophies[str(x)])

        self.writeVInt(0)
        for x in range(0):
            self.writeDataReference(16, x)
            self.writeVInt(0)

        self.writeVInt(len(self.player.brawlers_unlocked))
        for x in self.player.brawlers_unlocked:
            self.writeDataReference(16, x)
            self.writeVInt(self.player.brawlers_power_points[str(x)])

        self.writeVInt(len(self.player.brawlers_id))
        for x in self.player.brawlers_id:
            self.writeDataReference(16, x)
            self.writeVInt(self.player.brawlers_level[str(x)])

        self.writeVInt(len(self.player.brawlers_spg))
        for x in self.player.brawlers_spg:
            self.writeDataReference(23, x)
            self.writeVInt(1)

        self.writeVInt(0)  # New Brawlers Array
        for x in range(0):
            self.writeDataReference(16, x)
            self.writeVInt(0)

        self.writeVInt(self.player.gems) # Player Gems
        self.writeVInt(self.player.gems) # Player Free Gems

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeVInt(3) # Tutorial State
