import asyncio
import threading
import importlib
import pkgutil
from Core.Networking.Server import Server
from Config import load_config
import Config
from Utils.Logger import Logger
import websockets

# ------------------------
# Console command loader
# ------------------------
class ConsoleCommands:
    def __init__(self):
        self.commands = {}
        self.load_commands()

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


# ------------------------
# WebSocket console handler
# ------------------------
async def handle_console(websocket, path, server, command_registry):
    addr = websocket.remote_address
    Logger.log("debug", f"Web console connected from {addr}")

    try:
        async for message in websocket:
            line = message.strip()
            if not line:
                continue

            parts = line.split()
            cmd_name, args = parts[0], parts[1:]
            cmd_obj = command_registry.get(cmd_name)

            if cmd_obj:
                try:
                    # pass websocket into command
                    await cmd_obj.execute(server, websocket, *args)
                except Exception as e:
                    await websocket.send(f"Error executing {cmd_name}: {e}")
            else:
                await websocket.send(f"Unknown command: {cmd_name}")
    finally:
        Logger.log("debug", f"Web console disconnected: {addr}")

# ------------------------
# Start WebSocket console server in a thread
# ------------------------
def start_console_server(server, command_registry, host="127.0.0.1", port=8765):
    async def handle_connection(websocket):
        # Just pass None for path since v11+ no longer sends it
        await handle_console(websocket, None, server, command_registry)

    async def main():
        async with websockets.serve(handle_connection, host, port):
            Logger.log("*", f"Web console listening on ws://{host}:{port}")
            await asyncio.Future()  # run forever

    def runner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.run_forever()

    # Start the WebSocket server in a daemon thread
    threading.Thread(target=runner, daemon=True).start()

# ------------------------
# Main server app
# ------------------------
class Main:
    def __init__(self):
        load_config()
        self.useUpdater = Config.config.get("UpgradesEnabled", False)
        self.updater = None
        self.crashCount = 0

        print(Logger.yellow + Config.asciiart)

        self.run()

    def run(self):
        if self.useUpdater:
            from Utils.Updater import Updater
            self.updater = Updater()

        srv = Server("0.0.0.0", 9339)
        commands = ConsoleCommands()

        # Start server thread
        threading.Thread(target=srv.start, daemon=True).start()

        # Start websocket console server thread
        threading.Thread(target=start_console_server, args=(srv, commands), daemon=True).start()

        Logger.log("*", "Connect to console via WebSocket ws://127.0.0.1:8765")

        # Keep main thread alive
        try:
            while True:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            Logger.log("*", "Shutting down server...")
            srv.running = False


if __name__ == "__main__":
    Main()
