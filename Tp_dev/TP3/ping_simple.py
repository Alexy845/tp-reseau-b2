import os

adresse_ip = "8.8.8.8"
commande_ping = f"ping -n 4 {adresse_ip}"
os.system(commande_ping)
