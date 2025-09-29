import json, string, random
import Logic.Player
import re

class Helpers:
    connected_clients = {"ClientsCount": 0, "Clients": {}}

    def randomToken(self):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(40))

    def randomID(self, length = 8):
        return int(''.join([str(random.randint(0, 9)) for _ in range(length)]))

    def randomMapID(self):
        return random.randint(1, 2147483647)

    def get_box_type(self, id):
        if id == 5:  # Brawl Box
            return 10
        elif id == 4:  # Big Box
            return 12
        elif id == 3:  # Shop Mega Box
            return 11
        elif id == 1:  # Shop Big Box
            return 12

    def create_config(self):
        settings = {
                "MongoConnectionURL": "",
                "StarPoints": 5000,
                "Gold": 10000,
                "Gems": 100000,
                "Trophies": 0,
                "ExperiencePoints": 999999,
                "BrawlBoxTokens": 99999,
                "BigBoxTokens": 99999,
                "Region": "RO",
                "ThemeID": 0,
                "Maintenance": False,
                "SecondsTillMaintenanceOver": 3600
            }


        with open('config.json', 'w') as config_file:
            json.dump(settings, config_file)

    def load_club(self, club_data):
        try:
            self.player.message_tick = club_data['Messages'][-1]['Tick']
        except:
            pass
    
    @staticmethod
    def kick_player(client_id: str, kick_id = 1, reason: str = "Kicked by server"):
        from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage
        from Utils.Logger import Logger

        client_entry = Helpers.connected_clients["Clients"].get(client_id)

        if not client_entry:
            return False

        sock = client_entry["SocketInfo"]

        class FakePlayer:
            err_code = int(kick_id)
            patch_url = ""
            update_url = ""
            maintenance_time = 0

        player = FakePlayer()
        msg = LoginFailedMessage(sock, player, reason)
        msg.encode()
        msg.send()

        try:
            sock.close()
        except Exception as e:
            Logger.log("error", f"Error closing socket for {client_id}: {e}")

        del Helpers.connected_clients["Clients"][client_id]
        Helpers.connected_clients["ClientsCount"] -= 1

        Logger.log("client", f"Kicked client {client_id} – {reason}")
        return True

    @staticmethod
    def serialize_socket_info(socket_info):
        if socket_info is None or socket_info._closed:
            return "Socket closed"
        return {
            "local_address": socket_info.getsockname(),
            "remote_address": socket_info.getpeername() if socket_info.getpeername() else "Not connected"
        }

    @staticmethod
    def serialize_clients(clients):
        serialized_clients = {}
        for client_id, client_data in clients.items():
            serialized_clients[client_id] = {
                "SocketInfo": Helpers.serialize_socket_info(client_data['SocketInfo'])
            }
        return serialized_clients