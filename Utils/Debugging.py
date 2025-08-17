from ByteStream.Reader import Reader

class Debugging:
    @staticmethod
    def decode_n_dump(data):
        reader = Reader(data)
        output = "Decoded values: "
        while reader.offset < len(data):
            try:
                value = reader.readVInt()
                output += f"VInt: {value} "
            except:
                try:
                    ref = reader.readDataReference()
                    output += f"DataRef: {ref} "
                except:
                    try:
                        s = reader.readString()
                        output += f"String: {s} "
                    except:
                        output += "Unknown or end of data."
                        break
        print(output)