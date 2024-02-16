import asyncio
import argparse
import uuid

class MemcachedServer:

    """
    Memcached Server

    A simple Memcached server implementation using asyncio in Python.

    The server listens for incoming connections from clients and handles various Memcached commands,
    including SET, GET, ADD, REPLACE, APPEND, PREPEND, CAS (compare-and-swap), INCREMENT, and DECREMENT.

    Supported commands:
    - SET: Store data in the cache.
    - GET: Retrieve data from the cache.
    - ADD: Store data only if the key does not already exist.
    - REPLACE: Store data only if the key already exists.
    - APPEND: Append data to an existing key's value.
    - PREPEND: Prepend data to an existing key's value.
    - CAS: Compare and swap data based on a unique identifier.
    - INC: Increment the value of a numeric key.
    - DEC: Decrement the value of a numeric key.

    Usage:
    The server can be started with the specified port number and maximum cache size (optional).

    Example:
    python memcached_server.py -p 11211 -s 10000

    Arguments:
        -p, --port: Port number to run the server on (default: 11211).
        -s, --max-cache-size: Maximum cache size in bytes (default: unlimited).

    """

    def __init__(self, port, max_cache_size=None):
        self.port = port
        self.max_cache_size = max_cache_size
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
        elif command == 'ADD':
            await self.handle_add(command_parts, reader, writer)
        elif command == 'REPLACE':
            await self.handle_replace(command_parts, reader, writer)
        elif command == 'APPEND':
            await self.handle_append(command_parts, reader, writer)
        elif command == 'PREPEND':
            await self.handle_prepend(command_parts, reader, writer)
        elif command == 'CAS':
            await self.handle_cas(command_parts, reader, writer)
        elif command == 'INC':
            await self.handle_increment_decrement(command_parts, writer, 'increment')
        elif command == 'DEC':
            await self.handle_increment_decrement(command_parts, writer, 'decrement')
        else:
            writer.write(b'ERROR\r\n')

    async def handle_set(self, command_parts, reader, writer):
        if self.max_cache_size is not None and len(self.cache) >= self.max_cache_size:
            writer.write(b'SERVER_ERROR Cache size limit reached\r\n')
            return
        

        key = command_parts[1]
        try:
            byte_count = int(command_parts[4])
            value = await reader.readexactly(byte_count)
            
            unique_id = str(uuid.uuid4())
            self.cache[key] = {'value': value, 'cas_unique': unique_id}
            
            # Respond with STORED and the unique identifier
            writer.write(f'STORED {unique_id}\r\n'.encode())
        except (ValueError, asyncio.exceptions.IncompleteReadError):
            writer.write(b'CLIENT_ERROR\r\n')


    async def handle_get(self, command_parts, writer):
        key = command_parts[1]
        item = self.cache.get(key)
        if item:
            value = item['value']
            cas_unique = item['cas_unique']
            value_str = value.decode()  # Decode bytes to string
            writer.write(f'VALUE {key} 0 {len(value_str)} {cas_unique}\r\n{value_str}\r\nEND\r\n'.encode())
        else:
            writer.write(b'END\r\n')



    async def handle_cas(self, command_parts, reader, writer):
        key = command_parts[1]
        if key not in self.cache:
            writer.write(b'NOT_FOUND\r\n')
            return

        cas_unique = command_parts[-1]
        if cas_unique != self.cache[key]['cas_unique']:
            writer.write(b'EXISTS\r\n')
            return

        try:
            byte_count = int(command_parts[4])
            value = await reader.readexactly(byte_count)
            self.cache[key] = {'value': value, 'cas_unique': cas_unique}
            writer.write(b'STORED\r\n')
        except (ValueError, asyncio.exceptions.IncompleteReadError):
            writer.write(b'CLIENT_ERROR\r\n')



    async def handle_add(self, command_parts, reader, writer):
        key = command_parts[1]
        if key in self.cache:
            writer.write(b'NOT_STORED\r\n')
        else:
            await self.handle_set(command_parts, reader, writer)

    async def handle_replace(self, command_parts,reader, writer):
        key = command_parts[1]
        if key in self.cache:
            await self.handle_set(command_parts, reader, writer)
        else:
            writer.write(b'NOT_STORED\r\n')


    async def handle_append(self, command_parts, reader, writer):
        key = command_parts[1]
        if key not in self.cache:
            writer.write(b'NOT_STORED\r\n')
            return

        try:
            byte_count = int(command_parts[4])
            value = await reader.readexactly(byte_count)
            self.cache[key] += value
            writer.write(b'STORED\r\n')
        except (ValueError, asyncio.exceptions.IncompleteReadError):
            writer.write(b'CLIENT_ERROR\r\n')

    async def handle_prepend(self, command_parts, reader, writer):
        key = command_parts[1]
        if key not in self.cache:
            writer.write(b'NOT_STORED\r\n')
            return

        try:
            byte_count = int(command_parts[4])
            value = await reader.readexactly(byte_count)
            self.cache[key] = value + self.cache[key]
            writer.write(b'STORED\r\n')
        except (ValueError, asyncio.exceptions.IncompleteReadError):
            writer.write(b'CLIENT_ERROR\r\n')


    async def handle_increment_decrement(self, command_parts, writer, operation):
        key = command_parts[1]
        if key not in self.cache:
            writer.write(b'NOT_FOUND\r\n')
            return

        try:
            delta = int(command_parts[2])
            current_value = self.cache.get(key, {'value': 0})  # Get the current value or 0 if not found
            
            if isinstance(current_value['value'], int):
                value = current_value['value']
            else:
                value = int(current_value['value'].decode()) 
            
            if isinstance(value, int):
                if operation == 'increment':
                    new_value = value + delta
                elif operation == 'decrement':
                    new_value = value - delta
                self.cache[key] = {'value': new_value, 'cas_unique': str(uuid.uuid4())}  # Update cache with new value and new CAS identifier
                writer.write(f'{new_value}\r\n'.encode())
            else:
                writer.write(b'CLIENT_ERROR\r\n')  # Value is not an integer
        except ValueError:
            writer.write(b'CLIENT_ERROR\r\n')  # Delta is not a valid integer






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Memcached Server')
    parser.add_argument('-p', '--port', type=int, default=11211, help='Port number (default: 11211)')
    parser.add_argument('-s', '--max-cache-size', type=int, default=None, help='Maximum cache size (default: unlimited)')
    args = parser.parse_args()

    server = MemcachedServer(args.port, max_cache_size=args.max_cache_size)
    asyncio.run(server.start())
