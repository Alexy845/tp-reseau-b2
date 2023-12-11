import socket
import sys

host = '10.1.2.22'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

texte = input("Que veux-tu envoyer au serveur : ")

try:
    s.sendall(texte.encode())
    data = s.recv(1024)
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
except socket.error:
    print("Error Occured.")
    sys.exit(1)
    
print(f"Le serveur a répondu {repr(data.decode())}")
sys.exit(0)