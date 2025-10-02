# Core/Message/GameMessage.py
from ByteStream.Reader import Reader
from ByteStream.Writer import Writer

class GameMessage:
    def __init__(self, client=None, data: bytes = None):
        """
        :param client: Optional socket/client to send data through
        :param data: Optional raw bytes to read from
        """
        self.reader: Reader | None = Reader(data) if data else None
        self.writer: Writer | None = Writer(client) if client else None
        self._version: int = 0

    # ----------------
    # Encoding/Decoding
    # ----------------
    def encode(self):
        """Override in subclass to write to self.writer"""
        pass

    def decode(self):
        """Override in subclass to read from self.reader"""
        pass

    # ----------------
    # Abstract methods
    # ----------------
    def get_message_type(self) -> int:
        """Override in subclass"""
        raise NotImplementedError

    def get_service_node_type(self) -> int:
        """Override in subclass"""
        raise NotImplementedError

    # ----------------
    # Version
    # ----------------
    def set_version(self, version: int):
        self._version = version

    def get_version(self) -> int:
        return self._version

    # ----------------
    # Accessors
    # ----------------
    def get_reader(self) -> Reader | None:
        return self.reader

    def get_writer(self) -> Writer | None:
        return self.writer

    def get_message_bytes(self) -> bytes:
        if self.writer:
            return self.writer.getRaw()
        return b''

    def get_encoding_length(self) -> int:
        if self.writer:
            return self.writer.size()
        return 0
