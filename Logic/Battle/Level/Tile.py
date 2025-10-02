from typing import Optional
from Logic.Data.DataTables import DataTables
from Logic.Data.DataType import DataType
from Logic.Data.Helper.TileData import TileData

class Tile:
    def __init__(self, code: str, x: int, y: int):
        self.code: str = code
        self.x: int = x
        self.y: int = y

        self.data: Optional[TileData] = None
        self.destructed: bool = False

        # Match C# constructor logic
        for data in DataTables.get(DataType.TILE).datas:
            if isinstance(data, TileData):
                if data.tile_code[0] == code:
                    self.data = data
                    break

        if self.data is None:
            self.data = DataTables.get(DataType.TILE).get_data(0)

    @staticmethod
    def tile_code_to_instance_id(code: str) -> int:
        # Switch block in C# only had default case (-1)
        return -1

    def destruct(self):
        self.destructed = True

    def is_destructed(self) -> bool:
        return self.destructed

    def get_check_sum(self) -> int:
        # Stub, same as C#
        return 0