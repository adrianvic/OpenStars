from dataclasses import dataclass
from typing import List

@dataclass
class Row:
    """Represents a row in a CSV table"""
    offset: int
    table: 'Table'
    values: List[str]
    
    def get_name(self) -> str:
        """Get the name of this row (first column value)"""
        return self.values[0] if self.values else ""
    
    def get_value(self, column_index: int) -> str:
        """Get value at specific column index"""
        if 0 <= column_index < len(self.values):
            return self.values[column_index]
        return ""
    
    def get_int(self, column_index: int) -> int:
        """Get integer value at column index"""
        try:
            return int(self.get_value(column_index))
        except (ValueError, TypeError):
            return 0
    
    def get_float(self, column_index: int) -> float:
        """Get float value at column index"""
        try:
            return float(self.get_value(column_index))
        except (ValueError, TypeError):
            return 0.0
    
    def get_bool(self, column_index: int) -> bool:
        """Get boolean value at column index"""
        val = self.get_value(column_index).lower()
        return val in ['true', '1', 'yes']

    def get_value_by_name(self, column_name: str) -> str:
        """Get value by column name"""
        idx = self.table.get_column_index_by_name(column_name)
        if idx == -1:
            return ""
        return self.get_value(idx)

    def get_int_by_name(self, column_name: str) -> int:
        try:
            return int(self.get_value_by_name(column_name))
        except (ValueError, TypeError):
            return 0

    def get_bool_by_name(self, column_name: str) -> bool:
        val = self.get_value_by_name(column_name).lower()
        return val in ["true", "1", "yes"]