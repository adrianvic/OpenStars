class Command:
    def __init__(self):
        self.name = "reload"

    def execute(self, server, *args):
        from Utils.Logger import Logger
        Logger.log("*", "Reloading server...")
        # Add reload logic here
