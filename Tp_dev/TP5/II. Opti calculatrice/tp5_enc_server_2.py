import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 9999))
sock.listen()
client, client_addr = sock.accept()

while True:
    # On lit les 2 premiers octets qui arrivent du client
    # Car dans le client, on a fixé la taille du header à 2 octets
    header = client.recv(2)
    if not header:
        break

    # On lit la valeur
    msg_len = int.from_bytes(header, byteorder='big')

    print(f"Lecture des {msg_len} prochains octets")

    # Une liste qui va contenir les données reçues
    chunks = []

    bytes_received = 0
    while bytes_received < msg_len:
        # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
        chunk = client.recv(min(msg_len - bytes_received, 1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')

        # on ajoute le morceau de 1024 ou moins à notre liste
        chunks.append(chunk)

        # on ajoute la quantité d'octets reçus au compteur
        bytes_received += len(chunk)

    # Assembler la liste en un seul message
    encoded_message = b"".join(chunks)

    # Décoder le message en UTF-8 pour obtenir l'expression mathématique
    expression = encoded_message.decode('utf-8')
    print(f"Received from client: {expression}")

    # Splitter l'expression pour obtenir les éléments
    elements = expression.split()
    num1 = int(elements[0])
    operation = elements[1]
    num2 = int(elements[2])

    # Évaluation de l'expression
    try:
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        else:
            raise ValueError("Opération non supportée")

        # Conversion du résultat en chaîne de caractères
        result_str = str(result)
    except Exception as e:
        result_str = "Erreur: " + str(e)

    # Encodage du résultat en UTF-8 pour l'envoi
    encoded_result = result_str.encode('utf-8')

    # Taille du résultat encodé sur 2 octets
    result_len = len(encoded_result).to_bytes(2, byteorder='big')

    # Lecture de la séquence de fin
    end_sequence = client.recv(8)  # Taille de "<clafin>" en bytes

    # Envoi du résultat encodé au client
    client.send(result_len + encoded_result)

    # Vérification de la séquence de fin
    if end_sequence == b"<clafin>":
        print(f"Message reçu du client : {expression}")
    else:
        print("Séquence de fin incorrecte")

client.close()
