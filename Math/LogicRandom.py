from Utils.Reader import Reader
from Utils.Writer import Writer

class LogicRandom:
    def __init__(self, seed: int = 0):
        self.seed = seed

    def get_iterated_random_seed(self) -> int:
        return self.seed

    def set_iterated_random_seed(self, value: int):
        self.seed = value

    def rand(self, max_value: int) -> int:
        if max_value > 0:
            self.seed = self.iterate_random_seed()
            tmp_val = abs(self.seed)
            return tmp_val % max_value
        return 0

    def iterate_random_seed(self) -> int:
        seed = self.seed
        if seed == 0:
            seed = -1

        tmp = seed ^ (seed << 13) ^ ((seed ^ (seed << 13)) >> 17)
        tmp2 = tmp ^ (32 * tmp)
        return tmp2

    # Encode/Decode using Writer/Reader
    def decode(self, reader: Reader):
        self.seed = reader.readVInt()

    def encode(self, writer: Writer):
        writer.writeVInt(self.seed)
