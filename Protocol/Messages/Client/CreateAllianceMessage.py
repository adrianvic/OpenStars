from ByteStream.Reader import Reader
from Utils.Helpers import Helpers
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceResponseMessage import AllianceResponseMessage
from Protocol.Messages.Server.AllianceDataMessage import AllianceDataMessage


class CreateAllianceMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.club_name            = self.readString()
        self.club_desc            = self.readString()
        self.club_badge           = self.readDataReference()[1]
        self.club_region          = self.readDataReference()[1]
        self.club_type            = self.readVInt()
        self.club_req_trophies    = self.readVInt()
        self.club_family_friendly = self.readVInt()

    def process(self, db):
        data = {
            "name": self.club_name,
            "description": self.club_desc,
            "region": self.club_region,
            "badge_id": self.club_badge,
            "type": self.club_type,
            "trophies": self.player.trophies,
            "required_trophies": self.club_req_trophies,
            "family_friendly": self.club_family_friendly,
            "members": [
                {
                 'name': self.player.name,
                 'ID': self.player.ID,
                 'role': 2,
                 'trophies': self.player.trophies,
                 'profile_icon': self.player.profile_icon,
                 'name_color': self.player.name_color
                 }
            ],
            "messages": []
        }

        self.player.club_id = Helpers.randomID(self)
        self.player.club_role = 2

        db.create_club(self.player.club_id, data)
        club_data = db.load_club(self.player.club_id)

        MyAllianceMessage(self.client, self.player, club_data).send()
        AllianceResponseMessage(self.client, self.player, 20).send()
        AllianceDataMessage(self.client, self.player, club_data).send()

