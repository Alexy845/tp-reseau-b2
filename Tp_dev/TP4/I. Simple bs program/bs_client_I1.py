import socket
import sys

host = '10.1.2.22'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

s.sendall(b"Meooooo !")

data = s.recv(1024)
s.close()

if not data:
    print("Pas de réponse du serveur.")
    sys.exit(1)

print(f"Le serveur a répondu {repr(data)}")
sys.exit(0)