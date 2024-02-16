class MessageSerializer:
    
    """
    A class to serialize and deserialize messages according to the Redis protocol.
    """ 
    @staticmethod
    def serialize_message(message):
        
        """
        Serialize a Python object into a Redis protocol-compliant string.
        """
        if isinstance(message, str):
            return f"+{message}\r\n"
        elif isinstance(message, bytes):
            return f"${len(message)}\r\n{message.decode()}\r\n"
        elif isinstance(message, (list, tuple)):
            serialized_items = [f"${len(item)}\r\n{item}\r\n" for item in message]
            return f"*{len(serialized_items)}\r\n{''.join(serialized_items)}"
        else:
            raise ValueError("Unsupported message type")

    @staticmethod
    def deserialize_message(serialized_message):
        
        """
        Deserialize a Redis protocol string into a Python object.
        """
        if serialized_message.startswith("+"):
            return serialized_message[1:].strip()
        elif serialized_message.startswith("-"):
            return serialized_message[1:].strip()
        elif serialized_message.startswith("$"):
            length_end = serialized_message.find("\r\n")
            length = int(serialized_message[1:length_end])
            data_start = length_end + 2
            data_end = data_start + length
            return serialized_message[data_start:data_end]
        elif serialized_message.startswith("*"):
            items = []
            serialized_items = serialized_message.split("\r\n")
            num_items = int(serialized_items[0][1:])
            for i in range(1, len(serialized_items) - 1, 2):
                length = int(serialized_items[i][1:])
                data = serialized_items[i + 1]
                items.append(data[:length])
            return items
        else:
            raise ValueError("Invalid serialized message")



