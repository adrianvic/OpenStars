from Logic.Data.DataTables import GlobalId, LogicData
from typing import Iterable

def write_data_reference(writer, data_or_id):
    """
    Write a data reference to the writer.
    Accepts either a LogicData instance or a global ID (int).
    """
    if data_or_id is None:
        writer.writeVInt(0)
        return

    if isinstance(data_or_id, LogicData):
        writer.writeVInt(data_or_id.get_class_id())
        writer.writeVInt(data_or_id.get_instance_id())
    elif isinstance(data_or_id, int):
        if data_or_id <= 0:
            writer.writeVInt(0)
        else:
            writer.writeVInt(GlobalId.get_class_id(data_or_id))
            writer.writeVInt(GlobalId.get_instance_id(data_or_id))
    else:
        raise TypeError(f"Unsupported type for data reference: {type(data_or_id)}")


def read_data_reference(reader) -> int:
    """
    Read a data reference from the reader and return a global ID.
    """
    class_id = reader.readVInt()
    if class_id <= 0:
        return 0
    instance_id = reader.readVInt()
    return GlobalId.create_global_id(class_id, instance_id)


def write_int_list(writer, int_list: Iterable[int]):
    """
    Write a list of integers using VInt encoding.
    """
    array = list(int_list)
    writer.writeVInt(len(array))
    for value in array:
        writer.writeVInt(value)