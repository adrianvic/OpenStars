import pkgutil
import importlib
from Utils.Logger import Logger

class ConsoleCommands:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConsoleCommands, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.commands = {}
        self.load_commands()
        self._initialized = True

    def load_commands(self):
        import Protocol.ConsoleCommands as CommandsModule
        for _, module_name, _ in pkgutil.iter_modules(CommandsModule.__path__):
            module = importlib.import_module(f"Protocol.ConsoleCommands.{module_name}")
            if hasattr(module, "Command"):
                cmd_cls = module.Command()
                self.commands[cmd_cls.name] = cmd_cls
        Logger.log("debug", f"Loaded console commands: {list(self.commands.keys())}")

    def get(self, name):
        return self.commands.get(name)

def get_console_commands():
    return ConsoleCommands()

class CommandContext:
    def __init__(self, server, source=None, websocket=None, player=None, client=None):
        self.server = server
        self.source = source
        self.websocket = websocket
        self.player = player
        self.client = client

    async def send(self, message):
        """Send feedback back to the source."""
        if self.websocket:
            await self.websocket.send(message)
        elif self.player:
            # send as a system message in alliance chat
            from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage
            system_msg = {'Event': 2, 'Message': message, 'PlayerID': 0, 'PlayerName': '[Server]', 'PlayerRole': 0, 'Tick': self.player.message_tick}
            AllianceStreamMessage(self.client, self.player, [system_msg]).sendByID(self.player.ID)
        else:
            Logger.log("console", message)