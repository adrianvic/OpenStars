from Logic.Data.LogicData import LogicData

class ItemData(LogicData):
    def __init__(self, row, datatable):
        super().__init__(row, datatable)
        self.load_data(self, type(self), row)

        self.name: str = ""
        self.parent_item_for_skin: str = ""
        self.file_name: str = ""
        self.export_name: str = ""
        self.export_name_enemy: str = ""
        self.shadow_export_name: str = ""
        self.ground_glow_export_name: str = ""
        self.looping_effect: str = ""
        self.value: int = 0
        self.value2: int = 0
        self.trigger_range_sub_tiles: int = 0
        self.trigger_area_effect: str = ""
        self.can_be_picked_up: bool = False
        self.spawn_effect: str = ""
        self.activate_effect: str = ""
        self.scw: str = ""
        self.scw_enemy: str = ""
        self.layer: str = ""