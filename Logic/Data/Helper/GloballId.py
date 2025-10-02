class GlobalId:
    @staticmethod
    def create_global_id(class_id: int, instance_id: int) -> int:
        return 1_000_000 + instance_id if class_id <= 0 else class_id * 1_000_000 + instance_id

    @staticmethod
    def get_class_id(global_id: int) -> int:
        return global_id // 1_000_000

    @staticmethod
    def get_instance_id(global_id: int) -> int:
        return global_id % 1_000_000