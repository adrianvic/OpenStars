class ClientInput:
    def __init__(self):
        self.index: int = 0
        self.type: int = 0
        self.x: int = 0
        self.y: int = 0
        self.auto_attack: bool = False
        self.auto_attack_target: int = 0
        self.owner_session_id: int = 0

    def decode(self, reader):
        self.index = reader.readPositiveIntMax32767()  # 15 bits
        self.type = reader.readPositiveIntMax15()      # 4 bits

        self.x = reader.readInt(15)
        self.y = reader.readInt(15)

        self.auto_attack = reader.readBool()

        if self.type == 9:  # use emote
            reader.readPositiveIntMax7()  # emote index (3 bits)

        if self.auto_attack:
            if reader.readBool():
                self.auto_attack_target = reader.readPositiveIntMax16383()  # 14 bits