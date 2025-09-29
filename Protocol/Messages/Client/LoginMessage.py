from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceWarMessage import AllianceWarMessage
from Utils.Helpers import Helpers
from Utils.Logger import Logger
from Clanker import Clanker
from Protocol.Messages.Server.LoginOkMessage import LoginOkMessage
from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage
from Protocol.Messages.Server.LobbyInfoMessage import LobbyInfoMessage
from Protocol.Messages.Server.OwnHomeDataMessage import OwnHomeDataMessage
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage

class LoginMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.client = client
        self.player = player
        self.helpers = Helpers()

    def decode(self):
        self.account_id = self.readLong()
        self.account_token = self.readString()
        self.game_major = self.readInt()
        self.game_minor = self.readInt()
        self.game_build = self.readInt()
        self.fingerprint_sha = self.readString()

    def process(self, db):
        if self.player.status == 3: return # already logged in

        # maintenance check
        if self.player.maintenance:
            self.player.err_code = 10
            LoginFailedMessage(self.client, self.player, None).send()
            return

        # patch/fingerprint check
        if self.fingerprint_sha != self.player.patch_sha and self.player.patch:
            self.player.err_code = 7
            LoginFailedMessage(self.client, self.player, None).send()
            return

        # create account
        if self.account_id == 0:
            # new account, create it
            self.player.ID = self.helpers.randomID()
            self.player.token = self.helpers.randomToken()
            db.create_player_account(self.player.ID, self.player.token)
        else:
            self.player.ID = self.account_id
            self.player.token = self.account_token
            Logger.log("debug", f"LoginMessage.process: account_id={self.account_id} account_token={self.account_token} player.ID={self.player.ID}")
            
        # mark logged in
        self.player.status = 3
        resulting_player = Clanker.get_or_create(self.player.ID, db)

        # should be using a helper function to create the player then pass to kick_player !!!
        if not resulting_player:
            class FakePlayer:
                err_code = int(1)
                patch_url = ""
                update_url = ""
                maintenance_time = 0

            player = FakePlayer()
            msg = LoginFailedMessage(self.client, player, "Account not found in the database.")
            msg.send()
            return

        self.player.load_from_data(resulting_player.to_dict())
        self.player.ID = resulting_player.ID
        self.player.token = resulting_player.token
        self.player.status = 3

        # send messages
        LoginOkMessage(self.client, self.player, self.player.ID, self.player.token).send()
        OwnHomeDataMessage(self.client, self.player).send()
        LobbyInfoMessage(self.client, self.player, 0).send() # Helpers.connected_clients['ClientsCount']

        # club messages
        if self.player.club_id != 0:
            club_data = db.load_club(self.player.club_id)
            MyAllianceMessage(self.client, self.player, club_data).send()
            if self.player.clubWarsEnabled:
                AllianceWarMessage(self.client, self.player).send()
            AllianceStreamMessage(self.client, self.player, club_data['messages']).send()