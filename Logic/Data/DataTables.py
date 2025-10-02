from __future__ import annotations
import os
import csv
from enum import Enum
from typing import Dict, List, Type, Optional
from dataclasses import dataclass

# --------------------------
# Row
# --------------------------
@dataclass
class Row:
    offset: int
    table: 'Table'
    values: List[str]

    def get_name(self) -> str:
        return self.values[0] if self.values else ""

    def get_value(self, column_index: int) -> str:
        if 0 <= column_index < len(self.values):
            return self.values[column_index]
        return ""

    def get_int(self, column_index: int) -> int:
        try:
            return int(self.get_value(column_index))
        except (ValueError, TypeError):
            return 0

    def get_bool(self, column_index: int) -> bool:
        val = self.get_value(column_index).lower()
        return val in ['true', '1', 'yes']

    def get_value_by_name(self, column_name: str) -> str:
        idx = self.table.get_column_index_by_name(column_name)
        return self.get_value(idx) if idx != -1 else ""

# --------------------------
# Table
# --------------------------
class Table:
    def __init__(self, csv_path: str):
        self.headers: List[str] = []
        self.types: List[str] = []
        self.rows: List[Row] = []
        self.columns: List[List[str]] = []

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.headers = next(reader)
            self.types = next(reader)
            self.columns = [[] for _ in self.headers]

            for i, row_data in enumerate(reader):
                if not row_data or not row_data[0]:
                    continue
                row = Row(i, self, row_data)
                self.rows.append(row)
                for j, val in enumerate(row_data):
                    self.columns[j].append(val)

    def get_row_count(self) -> int:
        return len(self.rows)

    def get_row_at(self, index: int) -> Row:
        return self.rows[index] if 0 <= index < len(self.rows) else None

    def get_column_index_by_name(self, name: str) -> int:
        try:
            return self.headers.index(name)
        except ValueError:
            return -1

# --------------------------
# DataType Enum
# --------------------------
class DataType(Enum):
    PROJECTILE = 6
    ALLIANCE_BADGE = 8
    LOCATION = 15
    CHARACTER = 16
    AREA_EFFECT = 17
    ITEM = 18
    SKILL = 20
    CARD = 23
    TILE = 27
    PLAYER_THUMBNAIL = 28
    SKIN = 29
    MILESTONE = 39
    NAME_COLOR = 43
    SKIN_CONF = 44
    EMOTE = 52

# --------------------------
# GlobalId
# --------------------------
class GlobalId:
    @staticmethod
    def create_global_id(class_id: int, instance_id: int) -> int:
        return class_id * 1000000 + instance_id if class_id > 0 else 1000000 + instance_id

    @staticmethod
    def get_class_id(global_id: int) -> int:
        return global_id // 1000000

    @staticmethod
    def get_instance_id(global_id: int) -> int:
        return global_id % 1000000

# --------------------------
# LogicData base
# --------------------------
class LogicData:
    def __init__(self, row: Row, data_table: DataTable):
        self.row = row
        self.data_table = data_table
        self._data_type = -1
        self._id = -1

    def load_data(self, data: LogicData, data_type: int = -1):
        self._data_type = data_type
        self._id = GlobalId.create_global_id(self._data_type, self.data_table.count())
        self.row = data.row

    def get_data_type(self) -> int:
        return self._data_type

    def get_global_id(self) -> int:
        return self._id

    def get_instance_id(self) -> int:
        return GlobalId.get_instance_id(self._id)

    def get_class_id(self) -> int:
        return GlobalId.get_class_id(self._id)

    def get_name(self) -> str:
        return self.row.get_name() if self.row else ""

# --------------------------
# Example *Data classes
# --------------------------
class CharacterData(LogicData):
    pass

class SkillData(LogicData):
    pass

class ProjectileData(LogicData):
    pass

# --------------------------
# DataTable
# --------------------------
class DataTable:
    def __init__(self, data_type: DataType, table: Table = None):
        self.data_type = data_type
        self.datas: List[LogicData] = []
        if table:
            for i in range(table.get_row_count()):
                row = table.get_row_at(i)
                if row and row.get_name():
                    self.datas.append(LogicData(row, self))

    def count(self) -> int:
        return len(self.datas)

    def get_data(self, name: str) -> Optional[LogicData]:
        for d in self.datas:
            if d.get_name() == name:
                return d
        return None

    def get_data_with_id(self, id: int) -> Optional[LogicData]:
        inst_id = GlobalId.get_instance_id(id)
        return self.datas[inst_id] if 0 <= inst_id < len(self.datas) else None

    def get_instance_id(self, name: str) -> int:
        for i, d in enumerate(self.datas):
            if d.get_name() == name:
                return i
        return -1

# --------------------------
# Gamefiles manager
# --------------------------
class Gamefiles:
    def __init__(self):
        self._data_tables: Dict[int, DataTable] = {}

    def initialize(self, table: Table, data_type: DataType):
        dt = DataTable(data_type, table)
        self._data_tables[data_type.value] = dt

    def get(self, data_type: DataType) -> Optional[DataTable]:
        return self._data_tables.get(data_type.value)

    def get_by_id(self, table_id: int) -> Optional[DataTable]:
        return self._data_tables.get(table_id)

    def contains_table(self, table_id: int) -> bool:
        return table_id in self._data_tables

# --------------------------
# DataTables manager
# --------------------------
class DataTables:
    GAMEFILES: Dict[DataType, str] = {
        DataType.PROJECTILE: "GameAssetsReplication/csv_logic/projectiles.csv",
        DataType.ALLIANCE_BADGE: "GameAssetsReplication/csv_logic/alliance_badges.csv",
        DataType.LOCATION: "GameAssetsReplication/csv_logic/locations.csv",
        DataType.CHARACTER: "GameAssetsReplication/csv_logic/characters.csv",
        DataType.AREA_EFFECT: "GameAssetsReplication/csv_logic/area_effects.csv",
        DataType.ITEM: "GameAssetsReplication/csv_logic/items.csv",
        DataType.SKILL: "GameAssetsReplication/csv_logic/skills.csv",
        DataType.CARD: "GameAssetsReplication/csv_logic/cards.csv",
        DataType.TILE: "GameAssetsReplication/csv_logic/tiles.csv",
        DataType.PLAYER_THUMBNAIL: "GameAssetsReplication/csv_logic/player_thumbnails.csv",
        DataType.SKIN: "GameAssetsReplication/csv_logic/skins.csv",
        DataType.MILESTONE: "GameAssetsReplication/csv_logic/milestones.csv",
        DataType.NAME_COLOR: "GameAssetsReplication/csv_logic/name_colors.csv",
        DataType.SKIN_CONF: "GameAssetsReplication/csv_logic/skin_confs.csv",
        DataType.EMOTE: "GameAssetsReplication/csv_logic/emotes.csv",
    }
    DATA_TYPES: Dict[DataType, Type[LogicData]] = {
        DataType.CHARACTER: CharacterData,
        DataType.SKILL: SkillData,
        DataType.PROJECTILE: ProjectileData
    }
    TABLES: Optional[Gamefiles] = None

    @classmethod
    def load(cls):
        cls.TABLES = Gamefiles()
        for dt, csv_path in cls.GAMEFILES.items():
            if os.path.exists(csv_path):
                cls.TABLES.initialize(Table(csv_path), dt)

    @classmethod
    def create(cls, data_type: DataType, row: Row, data_table: DataTable) -> LogicData:
        cls_type = cls.DATA_TYPES.get(data_type, LogicData)
        obj = cls_type(row, data_table)
        obj._data_type = data_type.value
        obj._id = GlobalId.create_global_id(obj._data_type, data_table.count())
        return obj

    @classmethod
    def get(cls, data_type: DataType) -> Optional[DataTable]:
        return cls.TABLES.get(data_type) if cls.TABLES else None
