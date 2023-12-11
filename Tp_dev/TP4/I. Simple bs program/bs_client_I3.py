import socket
import sys
import re

host = '10.1.2.22'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))
texte = input("Veuillez saisir une chaîne de caractères : ")
if type(texte) is str:
    try:
        s.sendall(texte.encode())
        data = s.recv(1024)
        print(f"Connecté avec succès au serveur {host} sur le port {port}")
        
        if not isinstance(texte, str):
            raise TypeError("L'entrée n'est pas une chaîne de caractères")
        if not re.search(r"(waf|meo)", texte):
            raise ValueError("La chaîne saisie ne contient ni 'waf' ni 'meo'")
    except TypeError as e:
        print(f"Erreur : {e}")
    except ValueError as e:
        print(f"Erreur : {e}")
    except socket.error:
        print("Error Occured.")
        sys.exit(1)


print(f"Le serveur a répondu {repr(data.decode())}")
sys.exit(0)




