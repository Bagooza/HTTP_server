import socket
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)


script_dir = os.path.dirname(os.path.abspath(__file__))
htdocs_dir = os.path.join(script_dir, 'htdocs')  

while True:    
    client_connection, client_address = server_socket.accept()

    
    request = client_connection.recv(1024).decode()
    print(request)

    
    index_path = os.path.join(htdocs_dir, 'index.html')

    
    try:
        with open(index_path, 'r', encoding='utf-8') as fin:
            content = fin.read()
        status_line = 'HTTP/1.0 200 OK\r\n'
    except FileNotFoundError:
        content = '<h1>404 Not Found</h1><p>The page you requested is missing.</p>'
        status_line = 'HTTP/1.0 404 Not Found\r\n'

    
    headers = 'Content-Type: text/html; charset=UTF-8\r\n\r\n'
    response = status_line + headers + content

    
    client_connection.sendall(response.encode())
    client_connection.close()
