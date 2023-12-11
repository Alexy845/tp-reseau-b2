import sys
import os

if len(sys.argv) == 2:
    adresse_ip = sys.argv[1]
    commande_ping = f"ping -n 1 {adresse_ip} > NUL" 
    retour = os.system(commande_ping)

    if retour == 0:
        print("UP !")
    else:
        print("DOWN !")
