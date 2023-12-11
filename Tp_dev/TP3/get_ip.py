import psutil

def get_wifi_ip():
    try:
        # Obtenez toutes les informations d'interface réseau
        interfaces = psutil.net_if_addrs()
        
        # Parcourez les interfaces pour trouver celle de votre carte WiFi
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == psutil.AF_INET and "Wi-Fi" in interface:
                    return addr.address

        # Si aucune adresse IP n'est trouvée pour votre carte WiFi
        return "Adresse IP introuvable pour la carte Wi-Fi"

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    wifi_ip = get_wifi_ip()
    print(f"Adresse IP de la carte Wi-Fi : {wifi_ip}")
