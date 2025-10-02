from typing import List, Optional
from Logic.Data.DataTables import LogicData, DataType
from Logic.Data.DataTables import Row, DataTable

class LocationData(LogicData):
    """Represents location/map data from locations.csv"""
    
    def __init__(self, row: Row, data_table: DataTable):
        super().__init__(row, data_table)
        self.name: str = ""
        self.disabled: bool = False
        self.tid: str = ""
        self.bg_prefix: str = ""
        self.location_theme: str = ""
        self.ground_scw: str = ""
        self.campaign_ground_scw: str = ""
        self.environment_scw: str = ""
        self.icon_swf: str = ""
        self.icon_export_name: str = ""
        self.game_mode: str = ""
        self.allowed_maps: str = ""
        self.music: str = ""
        self.community_credit: str = ""
        
        self.load_data()
    
    def load_data(self, data: 'LogicData', data_type: int = -1):
        """Load data from CSV row"""
        super().load_data(data, data_type)
        
        if not self.row:
            return
            
        # Map CSV columns to properties
        self.name = self.row.get_value(0)
        self.disabled = self.row.get_bool(1)
        self.tid = self.row.get_value(2)
        self.bg_prefix = self.row.get_value(3)
        self.location_theme = self.row.get_value(4)
        self.ground_scw = self.row.get_value(5)
        self.campaign_ground_scw = self.row.get_value(6)
        self.environment_scw = self.row.get_value(7)
        self.icon_swf = self.row.get_value(8)
        self.icon_export_name = self.row.get_value(9)
        self.game_mode = self.row.get_value(10)
        self.allowed_maps = self.row.get_value(11)
        self.music = self.row.get_value(12)
        self.community_credit = self.row.get_value(13)
    
    def get_allowed_maps_list(self) -> List[str]:
        """Parse allowed maps string into list of map names"""
        if not self.allowed_maps:
            return []
        return [map_name.strip() for map_name in self.allowed_maps.split(',')]
    
    def is_enabled(self) -> bool:
        """Check if location is enabled"""
        return not self.disabled
    
    def get_game_mode_type(self) -> Optional[str]:
        """Get the game mode type"""
        return self.game_mode
    
    def __str__(self):
        return f"LocationData(name='{self.name}', game_mode='{self.game_mode}', enabled={self.is_enabled()})"
