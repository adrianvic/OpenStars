class LogicData:
    def __init__(self, row=None, data_table=None):
        self._data_type = None
        self._id = None
        self.data_table = data_table
        self.row = row

    def load_data(self, data, type_cls=None, row=None, data_type=-1):
        # data_type can be inferred from type_cls mapping if needed
        self._data_type = data_type if data_type != -1 else getattr(type_cls, "_type_id", -1)
        self._id = self.create_global_id(self._data_type, len(self.data_table) if self.data_table else 0)
        self.row = row
        if row:
            row.load_data(data)

    def get_data_type(self):
        return self._data_type

    def get_global_id(self):
        return self._id

    def get_instance_id(self):
        return self._id & 0xFFFFFF  # example; depends on your GlobalId scheme

    def get_class_id(self):
        return self._id >> 24  # example; depends on your GlobalId scheme

    def get_name(self):
        return self.row.get_name() if self.row else None

    @staticmethod
    def create_global_id(data_type, instance_id):
        return (data_type << 24) | (instance_id & 0xFFFFFF)
