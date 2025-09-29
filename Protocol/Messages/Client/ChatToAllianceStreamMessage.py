from ByteStream.Reader import Reader
import asyncio
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage
from ConsoleCommands import get_console_commands, CommandContext

class ChatToAllianceStreamMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.msg = self.readString()

    def process(self, db):
        command_registry = get_console_commands()
        club_data = db.load_club(self.player.club_id)

        self.player.message_tick = club_data['Messages'][-1]['Tick'] if club_data['Messages'] else self.player.message_tick
        self.player.message_tick += 1

        message = {'Event': 2 ,'Message': self.msg, 'PlayerID': self.player.ID, 'PlayerName':self.player.name, 'PlayerRole':self.player.club_role, 'Tick': self.player.message_tick}

        smsg = self.msg.strip()
        if smsg.startswith("/"):
            parts = smsg[1:].split()
            cmd_name, args = parts[0], parts[1:]
            cmd_obj = get_console_commands().get(cmd_name)
            if cmd_obj:
                ctx = CommandContext(db, source="chat", player=self.player, client=self.client)
                asyncio.run(cmd_obj.execute(ctx, *args))
                return


        club_data['Messages'].append(message)
        db.update_club(self.player.club_id, 'Messages', club_data['Messages'])

        for member in club_data['Members']:
            member_id = member['ID']
            AllianceStreamMessage(self.client, self.player, [message]).sendByID(member_id)