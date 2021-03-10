from . import greeting

def send():
    return b'HTTP/1.1 200 OK \r\n Content-type: text/html; charset=utf-8 \r\n Connection: close \r\n\r\n <h1>hello</h1>'