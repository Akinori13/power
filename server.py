import socket
import traceback
import settings
import os

class Server:
    host = settings.SERVER['host']
    port = settings.SERVER['port']
    backlog = settings.SERVER['listen_backlog']
    bufsize = settings.SERVER['bufsize']

    def run(self):
        print('Running server...')
        try:
            # Create server_socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(self.backlog)

            while True:
                # Waiting for client connection
                print('Waiting for client connection...')
                # Get client connection and address
                (connection, address) = server_socket.accept()
                print('address:' + str(address))

                try:
                    # Get request
                    request = Request(connection.recv(self.bufsize))

                    # Create response
                    response = Response(request.method, request.target)

                    connection.send(response.get_context())
                except Exception:
                    traceback.print_exc()
                finally:
                    connection.close()
        finally:
            print('Stopped server')

class Response():
    REASON_PHRASES = {
        200: 'OK',
        404: 'Not Found'
    }

    MEDIA_TYPES = {
        'html': 'text/html; charset=utf-8',
        'css': 'text/css',
        'javascript': 'text/javascript',
        'json': 'application/json',
        'jpg': 'image/jpg',
        'png': 'image/png'
    }

    def __init__(self, method: str, target: str) -> None:
        self.http_version = 'HTTP/1.1'
        self.method = method
        if self.method == 'GET':
            file_path = settings.SERVER['document_root'] + '/' + target
            with open(file_path, 'rb') as f:
                self.body = f.read()
                self.status_code = 200
            if '.' in file_path:
                extension = file_path.rsplit(".", maxsplit=1)[-1]
                self.content_type = self.MEDIA_TYPES.get(extension, 'application/octet-stream')
        else:
            self.body = b''
            self.status_code = 404
        self.reason_phrase = self.REASON_PHRASES[self.status_code]
        self.headers = {
            'Connection': 'close',
            'Content-Language': 'ja',
            'Content-Length': f'{len(self.body)}',
            'Host': 'Power',
            'Content-Type': self.content_type
        }

    def get_context(self) -> bytes:
        start_line = f'{self.http_version} {self.status_code} {self.reason_phrase}'
        response_header = ''
        for field_name, field_value in self.headers.items():
            response_header += f'{field_name}: {field_value}\r\n'
        response_body = self.body
        context = (start_line + response_header + '\r\n').encode('UTF-8') + response_body
        return context

class Request():
    def __init__(self, data: bytes) -> None:
        coverd_start_line, remain = data.split(sep=b'\r\n', maxsplit=1)
        coverd_headers, coverd_body = remain.split(sep=b'\r\n\r\n', maxsplit=1)

        # Parse coverd_request_line
        self.method, self.target, self.http_version = coverd_start_line.decode('UTF-8').split(sep=' ')

        # Parse coverd_headers
        self.headers = {}
        for header_field in coverd_headers.decode('UTF-8').split(sep='\r\n'):
            field_name, field_value = header_field.split(sep=r': ')
            self.headers[field_name] = field_value
        
        # Parse coverd_body
        self.body = coverd_body.decode('UTF-8')
        


if __name__ == "__main__":
    server = Server()
    server.run()
