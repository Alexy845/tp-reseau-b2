import socket
import os

HOST = '127.0.0.1'
PORT = 8080

def create_http_response():
    base_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_path, 'index.html')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        http_response = f'''HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
                            {content}
                        '''
    else:
        http_response = "HTTP/1.0 404 Not Found\r\n\r\n<h1>Page Not Found</h1>"

    return http_response

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

                if data.startswith(b"GET / HTTP/1.0"):
                    response = create_http_response()
                else:
                    response = "HTTP/1.0 404 Not Found\r\n\r\n<h1>Page Not Found</h1>"

                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()
