import argparse
import socket

class MemcachedServer:
    def __init__(self, port):
        self.port = port
        self.cache = {}

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', self.port))
        server_socket.listen(5)
        print(f'Memcached server started on port {self.port}')

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Connection from {client_address}')
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode().strip()
            print('Raw data %s' % data)
            if not data:
                break
            command_parts = data.split()
            print('command parts %s' % command_parts)
            command = command_parts[0].upper()
            if command == 'SET':
                key = command_parts[1]
                value = ' '.join(command_parts[2:])
                self.cache[key] = value
                client_socket.sendall(b'STORED\r\n')
            elif command == 'GET':
                key = command_parts[1]
                value = self.cache.get(key)
                if value:
                    response = f'Key: {key}\r\nValue: {len(value)}\r\n{value}\r\nEND\r\n'
                else:
                    response = 'END\r\n'
                client_socket.sendall(response.encode())
            else:
                client_socket.sendall(b'ERROR\r\n')
        client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Memcached Server')
    parser.add_argument('-p', '--port', type=int, default=11211, help='Port number (default: 11211)')
    args = parser.parse_args()

    server = MemcachedServer(args.port)
    server.start()
