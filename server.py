import socket
import traceback
import settings

class Server:
    host = settings.SERVER['host']
    port = settings.SERVER['port']

    def run(self):
        print('Running server...')
        try:
            # Create server_socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            while True:
                # Waiting for client connection
                print('Waiting for client connection...')
                # Get client connection and address
                (connection, address) = server_socket.accept()
                print('address:' + str(address))

                try:
                    # Get request
                    request = Request(connection.recv(4096))

                    # Create response
                    response_line = 'HTTP/1.1 200 OK \r\n'
                    response_body = b'<body><h1>Hello World!</h1></body>'
                    response_header = ''
                    response_header += 'Connection: close \r\n'
                    response_header += 'Content-Language: ja \r\n'
                    response_header += f'Content-Length: {len(response_body)} \r\n'
                    response_header += 'Content-Type: text/html; charset=UTF-8 \r\n'
                    response_header += 'Host: Power \r\n'
                    response = (response_line + response_header + '\r\n').encode('utf-8') + response_body
                    connection.send(response)
                except Exception:
                    traceback.print_exc()
                finally:
                    connection.close()
        finally:
            print('Stopped server')
    

class Request():
    def __init__(self, data) -> None:
        coverd_start_line, remain = data.split(sep=b'\r\n', maxsplit=1)
        coverd_headers, coverd_body = remain.split(sep=b'\r\n\r\n', maxsplit=1)

        # Parse coverd_request_line
        self.method, self.target, self.http_version = coverd_start_line.decode('UTF-8').split(sep=' ')

        # Parse coverd_headers
        self.headers = {}
        for header_field in coverd_headers.decode('UTF-8').split(sep='\r\n'):
            field_name, field_value = header_field.split(sep=r': ?')
            self.headers[field_name] = field_value
        
        # Parse coverd_body
        self.body = coverd_body.decode('UTF-8')
        


if __name__ == "__main__":
    server = Server()
    server.run()
