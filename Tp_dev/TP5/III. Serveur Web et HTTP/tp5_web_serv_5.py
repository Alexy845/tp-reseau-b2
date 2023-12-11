import socket
import os

HOST = '127.0.0.1'
PORT = 8080
DOCUMENT_ROOT = 'htdocs'

def get_requested_file(request):
    filename = request.split()[1].lstrip('/')
    filepath = os.path.join(DOCUMENT_ROOT, filename)

    if os.path.exists(filepath) and os.path.isfile(filepath):
        return filepath, filename
    else:
        return None, None

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server running on http://{HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                print('Received', repr(data))

                if data.startswith(b"GET"):
                    filepath, filename = get_requested_file(data.decode('utf-8'))
                    if filepath:
                        filesize = os.path.getsize(filepath)
                        conn.sendall(f"HTTP/1.0 200 OK\nContent-Length: {filesize}\n\n".encode())

                        with open(filepath, 'rb') as file:
                            chunk = file.read(1024)
                            while chunk:
                                conn.sendall(chunk)
                                chunk = file.read(1024)
                    else:
                        conn.sendall(b'HTTP/1.0 404 Not Found\n\n<h1>404 Not Found</h1>')
                else:
                    conn.sendall(b'HTTP/1.0 400 Bad Request\n\n<h1>400 Bad Request</h1>')

if __name__ == "__main__":
    start_server()
