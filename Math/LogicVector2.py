from ByteStream.Reader import Reader
from ByteStream.Writer import Writer
from math import cos, sin, radians, isqrt

class LogicVector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, other: "LogicVector2"):
        self.x += other.x
        self.y += other.y

    def subtract(self, other: "LogicVector2"):
        self.x -= other.x
        self.y -= other.y

    def multiply(self, other: "LogicVector2"):
        self.x *= other.x
        self.y *= other.y

    def clone(self) -> "LogicVector2":
        return LogicVector2(self.x, self.y)

    def is_equal(self, other: "LogicVector2") -> bool:
        return self.x == other.x and self.y == other.y

    def get_length(self) -> int:
        return isqrt(self.x**2 + self.y**2)

    def get_length_squared(self) -> int:
        return self.x**2 + self.y**2

    def get_distance(self, other: "LogicVector2") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return isqrt(dx*dx + dy*dy)

    def get_distance_squared(self, other: "LogicVector2") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx*dx + dy*dy

    def normalize(self, value: int) -> int:
        length = self.get_length()
        if length != 0:
            self.x = self.x * value // length
            self.y = self.y * value // length
        return length

    def rotate(self, degrees: int):
        rad = radians(degrees)
        new_x = int(self.x * cos(rad) - self.y * sin(rad))
        new_y = int(self.x * sin(rad) + self.y * cos(rad))
        self.x = new_x
        self.y = new_y

    def set(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_in_area(self, min_x: int, min_y: int, max_x: int, max_y: int) -> bool:
        return min_x <= self.x < min_x + max_x and min_y <= self.y < min_y + max_y

    # Reader/Writer serialization
    def encode(self, writer: Writer):
        writer.writeVInt(self.x)
        writer.writeVInt(self.y)

    def decode(self, reader: Reader):
        self.x = reader.readVInt()
        self.y = reader.readVInt()

    def __str__(self):
        return f"LogicVector2({self.x},{self.y})"
