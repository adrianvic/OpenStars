from ByteStream.Reader import Reader
import Config
from Protocol.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
from Protocol.Messages.Server.SetSupportedCreatorResponseMessage import SetSupportedCreatorResponseMessage
from Protocol.Commands.Server.LogicSetSupportedCreatorCommand import LogicSetSupportedCreatorCommand

class SetSupportedCreatorMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.creator_code = self.readString()

    def process(self, db):
        if self.creator_code in Config.config.get("ContentCreatorCodes"):
            self.player.supported_content_creator = self.creator_code
            AvailableServerCommandMessage(self.client, self.player, LogicSetSupportedCreatorCommand).send()
        else:
            SetSupportedCreatorResponseMessage(self.client, self.player).send()
