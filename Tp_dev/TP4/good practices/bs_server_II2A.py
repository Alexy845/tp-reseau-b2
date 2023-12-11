import argparse
import logging

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", action="store", type=int, default=13337, help="Port du serveur")

args = parser.parse_args()

if args.port < 0 or args.port > 65535:
    print("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535)")
    exit(1)
if args.port < 1024:
    print("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
    exit(2)


logging.info(f"Le serveur tourne sur <IP>:{args.port}")



