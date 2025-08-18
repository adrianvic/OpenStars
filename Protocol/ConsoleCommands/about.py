class Command:
    def __init__(self):
        self.name = "about"

    async def execute(self, server, websocket, *args):
        from Utils.Logger import Logger
        from Utils.Helpers import Helpers
        import Config
        await websocket.send(Config.asciiart)