from ByteStream.Writer import Writer
from Files.CsvLogic.Regions import Regions
from Logic.Avatar.LogicPlayerStats import LogicPlayerStats
from Clanker import Clanker

class PlayerProfileMessage(Writer):

    def __init__(self, client, player, requested_id, db):
        super().__init__(client)
        self.id = 24113
        self.player = player
        self.player_data = Clanker.get_or_create(requested_id, db)
        self.db = db

    def encode(self):
        self.writeLogicLong(self.player_data.ID)

        self.writeDataReference(0, 0)

        self.writeVInt(len(self.player_data.brawlers_unlocked))
        for x in self.player_data.brawlers_unlocked:
            # HeroEntry::encode
            self.writeDataReference(16, x)
            self.writeDataReference(0, 0)
            self.writeVInt(self.player_data.brawlers_trophies[str(x)])
            self.writeVInt(self.player_data.brawlers_highest_trophies[str(x)])
            self.writeVInt(self.player_data.brawlers_level[str(x)] + 2)

        self.playerStats = LogicPlayerStats.getPlayerStats(self)

        self.writeVInt(len(self.playerStats))
        for x in self.playerStats:
            self.writeVInt(list(self.playerStats.keys()).index(x) + 1)
            self.writeVInt(self.playerStats[x])

        # PlayerDisplayData::encode
        self.writeString(self.player_data.name)
        self.writeVInt(100) # Unknown
        self.writeVInt(28000000 + self.player_data.profile_icon)
        self.writeVInt(43000000 + self.player_data.name_color)

        club_data = self.db.load_club(self.player_data.club_id)
        if self.player_data.club_id != 0 and club_data is not None:
            self.writeBoolean(True)
            self.writeLong(club_data['ID'])
            self.writeString(club_data['name'])
            self.writeDataReference(8, club_data['badge_id'])
            self.writeVInt(club_data['type'])
            self.writeVInt(len(club_data['members']))
            self.writeVInt(club_data['trophies'])
            self.writeVInt(club_data['required_trophies'])
            self.writeDataReference(0, 0)
            self.writeString(Regions().get_region_string(club_data['region']))
            self.writeVInt(0)
            self.writeUInt8(0)
            self.writeDataReference(25, self.player_data.club_role)
        else:
            self.writeBoolean(False)
            self.writeVInt(0)
