import time
import json
import Config
from threading import *
from Logic.Player import Player
from Logic.Device import Device
from Utils.Logger import Logger
from Utils.Helpers import Helpers
from Clanker import Clanker
from Protocol.LogicLaserMessageFactory import packets
from Protocol.Messages.Server.LobbyInfoMessage import LobbyInfoMessage
from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage

class ClientThread(Thread):
    def __init__(self, client, address, db):
        super().__init__()
        self.client = client
        self.address = address
        self.db = db
        self.device = Device(self.client)
        self.player = Player(db=self.db)
        self.player.status = 0

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
        Clanker.remove(self.player.ID)


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
                    if self.address[0] in Config.config.get('BannedIPs'):
                        self.player.err_code = 11
                        LoginFailedMessage(self.client, self.player, 'Account banned!').send()


                    if packet_id in packets:
                        packet_name = packets[packet_id].__name__
                        if packet_name not in Config.config["DisabledPacketLogging"]: Logger.log("network client", f'ADDR: {self.address} PID: {self.player.ID} USR: {self.player.name} ID: {packet_id} = {packet_name} ({packet_length} bytes)')

                        message = packets[packet_id](self.client, self.player, packet_data)
                        message.decode()
                        message.process(self.db)

                        if packet_id == 10101:
                            Helpers.connected_clients["Clients"][str(self.player.ID)] = {"SocketInfo": self.client}

                    else:
                        Logger.log("warning", f'Unhandled Packet! ADDR {self.address} ID {packet_id} ({packet_length} bytes)')

                if time.time() - last_packet > 10:
                    self.on_disconnect()
                    break

        except (ConnectionAbortedError, ConnectionResetError, TimeoutError):
            self.on_disconnect()