from ByteStream.Writer import Writer
from Files.CsvLogic.Regions import Regions

class JoinableAllianceListMessage(Writer):

    def __init__(self, client, player, clubs):
        super().__init__(client)
        self.id = 24304
        self.player = player
        self.clubs = clubs

    def encode(self):
        self.writeVInt(len(self.clubs))

        for club in self.clubs:
            self.writeLong(club['ID'])
            self.writeString(club['name'])
            self.writeDataReference(8, club['badge_id'])
            self.writeVInt(club['type'])
            self.writeVInt(len(club['members']))
            self.writeVInt(club['trophies'])
            self.writeVInt(club['required_trophies'])
            self.writeDataReference(0, 0)
            self.writeString(Regions().get_region_string(club['region']))
            self.writeVInt(0)
            self.writeVInt(club['family_friendly'])