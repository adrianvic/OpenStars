from Utils.Reader import Reader
from Utils.Writer import Writer
from Utils.Math import LogicMath  # assuming you have LogicMath functions like GetAngle, Sqrt, etc.

class LogicVector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def destruct(self):
        self.x = 0
        self.y = 0

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def clone(self):
        return LogicVector2(self.x, self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def get_angle(self):
        return LogicMath.get_angle(self.x, self.y)

    def get_angle_between(self, x, y):
        return LogicMath.get_angle_between(LogicMath.get_angle(self.x, self.y), LogicMath.get_angle(x, y))

    def get_distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return LogicMath.sqrt(dx*dx + dy*dy)

    def get_distance_squared(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx*dx + dy*dy

    def get_distance_squared_to(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return dx*dx + dy*dy

    def get_length(self):
        return LogicMath.sqrt(self.x*self.x + self.y*self.y)

    def get_length_squared(self):
        return self.x*self.x + self.y*self.y

    def is_equal(self, other):
        return self.x == other.x and self.y == other.y

    def is_in_area(self, min_x, min_y, max_x, max_y):
        return min_x <= self.x < min_x + max_x and min_y <= self.y < min_y + max_y

    def multiply(self, other):
        self.x *= other.x
        self.y *= other.y

    def normalize(self, value):
        length = self.get_length()
        if length != 0:
            self.x = self.x * value // length
            self.y = self.y * value // length
        return length

    def rotate(self, degrees):
        new_x = LogicMath.get_rotated_x(self.x, self.y, degrees)
        new_y = LogicMath.get_rotated_y(self.x, self.y, degrees)
        self.x = new_x
        self.y = new_y

    def set(self, x, y):
        self.x = x
        self.y = y

    def subtract(self, other):
        self.x -= other.x
        self.y -= other.y

    # Reader/Writer replacements
    def decode(self, reader: Reader):
        self.x = reader.readVInt()
        self.y = reader.readVInt()

    def encode(self, writer: Writer):
        writer.writeVInt(self.x)
        writer.writeVInt(self.y)

    def __str__(self):
        return f"LogicVector2({self.x},{self.y})"
