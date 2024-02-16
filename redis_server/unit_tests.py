import unittest
from main import MessageSerializer

class TestMessageSerializer(unittest.TestCase):
    def test_serialize_string(self):
        serialized = MessageSerializer.serialize_message("hello world")
        self.assertEqual(serialized, "+hello world\r\n")

    def test_serialize_bytes(self):
        serialized = MessageSerializer.serialize_message(b"hello world")
        self.assertEqual(serialized, "$11\r\nhello world\r\n")

    def test_serialize_list(self):
        serialized = MessageSerializer.serialize_message(["get", "key"])
        self.assertEqual(serialized, "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n")

    def test_deserialize_string(self):
        deserialized = MessageSerializer.deserialize_message("+hello world\r\n")
        self.assertEqual(deserialized, "hello world")

    def test_deserialize_bytes(self):
        deserialized = MessageSerializer.deserialize_message("$11\r\nhello world\r\n")
        self.assertEqual(deserialized, "hello world")

    def test_deserialize_list(self):
        deserialized = MessageSerializer.deserialize_message("*2\r\n$3\r\nget\r\n$3\r\nkey\r\n")
        self.assertEqual(deserialized, ["get", "key"])

if __name__ == '__main__':
    unittest.main()
