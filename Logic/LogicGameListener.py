from Protocol.Messages.GameMessage import GameMessage

class LogicGameListener:
    def __init__(self):
        self.handled_inputs = 0

    def send_message(self, message: GameMessage):
        raise NotImplementedError("send_message must be implemented in a subclass")

    def send_tcp_message(self, message: GameMessage):
        raise NotImplementedError("send_tcp_message must be implemented in a subclass")
