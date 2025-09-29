import json
import socket
import Config
from Utils.Helpers import Helpers
from Utils.Logger import Logger
from DataBase.MongoDB import MongoDB
from DataBase.SQLDB import SQLDatabase
from Core.Networking.ClientThread import ClientThread
from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage

class Server:
    clients_count = 0

    def __init__(self, ip: str, port: int):
        self.db = MongoDB() if Config.config["DBBackend"] == 'mongodb' else SQLDatabase()
        # self.db.ensure_schema()
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # You can start server with the same address
        self.port = port
        self.ip = ip

    def start(self):
        self.server.bind((self.ip, self.port))
        Logger.log("*", f"Server started! Listening on {self.ip}:{self.port}")

        while True:
            self.server.listen()
            client, address = self.server.accept()
            Logger.log("connection", f"Client connected! IP: {address[0]}")
            ClientThread(client, address, self.db).start()
            Helpers.connected_clients['ClientsCount'] += 1