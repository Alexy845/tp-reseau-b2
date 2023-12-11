import sys
import os

if len(sys.argv) == 2:
    adresse_ip = sys.argv[1]
    commande_ping = f"ping {adresse_ip}"
    os.system(commande_ping)
