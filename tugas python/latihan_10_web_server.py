import socket

def handle_client(client_socket):
    while True:
        request = client_socket.recv(4096).decode('utf-8')
        if not request:
            break

        first_line = request.split('\n')[0]
        print("REQUEST:", first_line)
        ...

    try:
        filename = first_line.split()[1]
    except IndexError:
        client_socket.close()
        return

    if filename == '/':
        filename = '/index.html'

    filepath = filename.lstrip('/')

    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        # Tentukan Content-Type
        if filepath.endswith('.html'):
            mime_type = 'text/html'
        elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
            mime_type = 'image/jpeg'
        elif filepath.endswith('.png'):
            mime_type = 'image/png'
        else:
            mime_type = 'application/octet-stream'

        response_header = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {mime_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n\r\n"
            "Cache-Control: no-store\r\n"
        )

        client_socket.send(response_header.encode('utf-8') + content)
        print(f"[200] {filepath}")

    except FileNotFoundError:
        error_body = "<h1>404 Not Found</h1><p>File tidak ditemukan</p>"
        response_header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(error_body)}\r\n"
            "Connection: close\r\n\r\n"
        )

        client_socket.send(response_header.encode('utf-8') + error_body.encode('utf-8'))
        print(f"[404] {filepath}")

    client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)

    print("Web Server aktif di http://localhost:8080")

    while True:
        client, addr = server.accept()
        handle_client(client)

if __name__ == "__main__":
    run_server()