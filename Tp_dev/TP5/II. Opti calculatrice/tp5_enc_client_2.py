import socket
import re

def validate_expression(expression):
    pattern = r'^\d{1,5}\s*[+\-*]\s*\d{1,5}$'
    if re.match(pattern, expression):
        elements = re.split(r'\s*([+\-*])\s*', expression)
        num1 = int(elements[0])
        num2 = int(elements[2])
        if 0 <= num1 < 2**16 and 0 <= num2 < 2**16:
            return elements
    return None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 9999))

while True:
    user_input = input("Entrez une expression mathématique simple (x + ou - ou * y) : ")
    elements = validate_expression(user_input)
    if elements:
        break
    else:
        print("L'expression est invalide ou les nombres ne sont pas dans la plage de 2 octets.")

# À ce stade, elements contient les éléments valides de l'expression séparés
print("Expression valide :", elements)

# Calcul de la taille de l'expression en bytes
encoded_expression = ' '.join(elements).encode('utf-8')
expression_size = len(encoded_expression)

# Envoi de la taille de l'expression au serveur avant l'envoi de l'expression
size_header = expression_size.to_bytes(2, byteorder='big')
sock.send(size_header)

# Envoi de l'expression au serveur
sock.send(encoded_expression)

# Envoi de la séquence de fin
end_sequence = "<clafin>".encode('utf-8')
sock.send(end_sequence)

# Réception et affichage du résultat
result = sock.recv(1024).decode('utf-8')
print(f"Résultat: {result}")

sock.close()
