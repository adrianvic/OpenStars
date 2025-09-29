from ByteStream.Writer import Writer
from Files.CsvLogic.Regions import Regions

class AllianceDataMessage(Writer):

    def __init__(self, client, player, club_data):
        super().__init__(client)
        self.id = 24301
        self.player = player
        self.club_data = club_data

    def encode(self):
        print(self.club_data)
        if self.club_data:
            self.writeVInt(0)
            self.writeLong(self.club_data['ID'])
            self.writeString(self.club_data['name'])
            self.writeDataReference(8, self.club_data['badge_id'])
            self.writeVInt(self.club_data['type'])
            self.writeVInt(len(self.club_data['members']))
            self.writeVInt(self.club_data['trophies'])
            self.writeVInt(self.club_data['required_trophies'])
            self.writeDataReference(0, 0)
            self.writeString(Regions().get_region_string(self.club_data['region']))
            self.writeVInt(0)
            self.writeVInt(self.club_data['family_friendly'])

            self.writeString(self.club_data['description'])

            self.writeVInt(len(self.club_data['members']))

            for member in self.club_data['members']:
                self.writeLong(member['ID'])
                self.writeVInt(member['role'])
                self.writeVInt(member['trophies'])
                self.writeVInt(2) # Player Status
                self.writeVInt(0)
                self.writeVInt(0)

                self.writeString(member['name'])
                self.writeVInt(100)
                self.writeVInt(28000000 + member['profile_icon'])
                self.writeVInt(43000000 + member['name_color'])

        else:
            self.writeVInt(2)



