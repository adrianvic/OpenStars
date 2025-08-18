class Command:
    def __init__(self):
        self.name = "kick"

    async def execute(self, server, websocket, *args):
        from Utils.Helpers import Helpers
        from Utils.Logger import Logger

        if not args:
            await websocket.send("Usage: kick <player_id> <kick_id> [reason]")
            return

        player_id = args[0]
        kick_id = args[1]
        reason = " ".join(args[2:]) if len(args) > 2 else "Kicked."

        result = Helpers.kick_player(player_id, kick_id, reason)

        if (result):
            await websocket.send(Logger.log("consolecommand", f"Kicked {player_id} ({reason})", True))
        else: await websocket.send(Logger.log("error", f"Kick failed: no client with id {player_id}", True))