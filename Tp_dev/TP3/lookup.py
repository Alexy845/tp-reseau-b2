import sys
import socket

if len(sys.argv) == 2:
    nom_de_domaine = sys.argv[1]

    try:
        adresse_ip = socket.gethostbyname(nom_de_domaine)
        print(f"L'adresse IP de {nom_de_domaine} est : {adresse_ip}")
    except socket.gaierror:
        print(f"Impossible de résoudre {nom_de_domaine} en adresse IP.")
