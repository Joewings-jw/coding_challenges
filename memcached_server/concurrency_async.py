import asyncio
import argparse

class MemcachedServer:
    def __init__(self, port):
        self.port = port
        self.cache = {}

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client, '127.0.0.1', self.port)
        async with server:
            print(f'Memcached server started on port {self.port}')
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        client_address = writer.get_extra_info('peername')
        print(f'Connection from {client_address}')

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                await self.process_command(data, reader, writer)

            await writer.drain()

        except asyncio.CancelledError:
            print(f'Client connection from {client_address} cancelled.')
        finally:
            writer.close()

    async def process_command(self, data, reader, writer):
        command_parts = data.decode().split()
        if not command_parts:
            writer.write(b'ERROR\r\n')
            return

        command = command_parts[0].upper()
        if command == 'SET':
            await self.handle_set(command_parts, reader, writer)
        elif command == 'GET':
            await self.handle_get(command_parts, writer)

    async def handle_set(self, command_parts, reader, writer):
        key = command_parts[1]
        try:
            byte_count = int(command_parts[4])
            value = await reader.readexactly(byte_count)
            print('Set Value %s' % value)
            self.cache[key] = value
            writer.write(b'STORED\r\n')
        except (ValueError, asyncio.exceptions.IncompleteReadError):
            writer.write(b'CLIENT_ERROR\r\n')


    async def handle_get(self, command_parts, writer):
        key = command_parts[1]
        value = self.cache.get(key, b'')
        if value:
            print('value %s' % value)
            value_str = value.decode()  # Decode bytes to string
            writer.write(f'VALUE {key} 0 {len(value_str)}\r\n{value_str}\r\nEND\r\n'.encode())
        else:
            writer.write(b'END\r\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Memcached Server')
    parser.add_argument('-p', '--port', type=int, default=11211, help='Port number (default: 11211)')
    args = parser.parse_args()

    server = MemcachedServer(args.port)
    asyncio.run(server.start())
