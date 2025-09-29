class Command:
    def __init__(self):
        self.name = "about"

    async def execute(self, CommandContext, *args):
        from Utils.Logger import Logger
        from Utils.Helpers import Helpers
        import Config
        await CommandContext.send(Config.asciiart)