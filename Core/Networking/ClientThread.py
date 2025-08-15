import time
import json
from threading import *
from Logic.Player import Player
from Logic.Device import Device
from Utils.Logger import Logger
from Utils.Helpers import Helpers
from Protocol.LogicLaserMessageFactory import packets
from Protocol.Messages.Server.LobbyInfoMessage import LobbyInfoMessage
from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage

class ClientThread(Thread):
    def __init__(self, client, address, db):
        super().__init__()
        self.client = client
        self.address = address
        self.db = db
        self.config = json.loads(open('config.json', 'r').read())
        self.device = Device(self.client)
        self.player = Player(self.device)


    def recvall(self, length: int):
        data = b''

        while len(data) < length:
            s = self.client.recv(length)

            if not s:
                Logger.log("error", f"Error while receiving data!")
                break

            data += s
        return data

    def on_disconnect(self):
        Logger.log("debug", f"Client disconnected! IP: {self.address[0]}")
        self.client.close()
        Helpers.connected_clients['ClientsCount'] -= 1

    def run(self):
        try:
            last_packet = time.time()
            while True:
                header = self.client.recv(7)

                if len(header) > 0:

                    last_packet = time.time()

                    # Packet Info
                    packet_id = int.from_bytes(header[:2], 'big')
                    packet_length = int.from_bytes(header[2:5], 'big')
                    packet_data = self.recvall(packet_length)

                    # Ban
                    if self.address[0] in self.config['BannedIPs']:
                        self.player.err_code = 11
                        LoginFailedMessage(self.client, self.player, 'Account banned!').send()

                    LobbyInfoMessage(self.client, self.player, Helpers.connected_clients['ClientsCount']).send()

                    if packet_id in packets:
                        packet_name = packets[packet_id].__name__
                        Logger.log("client", f'PacketID: {packet_id}, Name: {packet_name} Length: {packet_length}')

                        message = packets[packet_id](self.client, self.player, packet_data)
                        message.decode()
                        message.process(self.db)

                        if packet_id == 10101:
                            Helpers.connected_clients["Clients"][str(self.player.ID)] = {"SocketInfo": self.client}

                    else:
                        Logger.log("client", f'Unhandled Packet! ID: {packet_id}, Length: {packet_length}')

                if time.time() - last_packet > 10:
                    self.on_disconnect()
                    break

        except (ConnectionAbortedError, ConnectionResetError, TimeoutError):
            self.on_disconnect()