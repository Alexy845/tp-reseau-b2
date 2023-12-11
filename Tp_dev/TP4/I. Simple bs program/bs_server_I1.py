import socket

host = ''
port = 13337 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

while True:

    try:
        data = conn.recv(1024)

        if not data: break

        print(f"Données reçues du client : {data}")

        conn.sendall("Salut mec.".encode())

    except socket.error:
        print("Error Occured.")
        break

conn.close()
