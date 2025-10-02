from typing import List, Optional

class Tile:
    def __init__(self, code: str, x: int, y: int):
        self.code = code   # char representing the tile type
        self.x = x         # logic coordinate X
        self.y = y         # logic coordinate Y

class TileMap:
    def __init__(self, width: int, height: int, data: str):
        self.width = width
        self.height = height

        self.spawn_points: List[Tile] = []
        self.spawn_points_team1: List[Tile] = []
        self.spawn_points_team2: List[Tile] = []

        chars = list(data)
        idx = 0

        # 2D grid [row][col] = Tile
        self.tiles: list[list[Tile]] = [[None for _ in range(width)] for _ in range(height)]

        for i in range(height):
            for j in range(width):
                tile = Tile(chars[idx], self.tile_to_logic(j), self.tile_to_logic(i))
                self.tiles[i][j] = tile

                if chars[idx] == '1':
                    self.spawn_points.append(tile)
                    self.spawn_points_team1.append(tile)
                elif chars[idx] == '2':
                    self.spawn_points.append(tile)
                    self.spawn_points_team2.append(tile)

                idx += 1

    @property
    def logic_width(self) -> int:
        return self.tile_to_logic(self.width)

    @property
    def logic_height(self) -> int:
        return self.tile_to_logic(self.height)

    def get_tile(self, x: int, y: int, is_tile: bool = False) -> Optional[Tile]:
        if not is_tile:
            x = self.logic_to_tile(x)
            y = self.logic_to_tile(y)

        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    @staticmethod
    def logic_to_tile(logic_value: int) -> int:
        return logic_value // 300

    @staticmethod
    def tile_to_logic(tile: int) -> int:
        return 300 * tile + 150

    def get_tiles(self) -> list[list[Tile]]:
        return self.tiles
