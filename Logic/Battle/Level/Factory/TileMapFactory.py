import json
from pathlib import Path
from Logic.Battle.Level.TileMap import TileMap


class TileMapFactory:
    # Load the JSON once, like the static field in C#
    with open(Path("GameAssetsReplication/tilemaps.json"), "r", encoding="utf-8") as f:
        _json_object = json.load(f)

    @staticmethod
    def create_tilemap(map_name: str) -> TileMap:
        obj = TileMapFactory._json_object.get(map_name)
        if obj is None:
            raise ValueError(f"Map '{map_name}' not found in tilemaps.json")

        return TileMap(
            int(obj["WIDTH"]),
            int(obj["HEIGHT"]),
            obj["Data"]
        )
