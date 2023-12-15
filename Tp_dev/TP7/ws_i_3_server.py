import asyncio
import websockets
from colorama import Fore, Style

host = '127.0.0.1'
port = 8888
global CLIENTS
CLIENTS = {}


async def handle_client_msg(websocket, path):
    addr = websocket.remote_address
    print(f"New client: {addr[0]}:{addr[1]}")

    message = await websocket.recv()
    pseudo = message.split("|")[1]
    print(f"{addr[0]}:{addr[1]} has chosen the pseudo {pseudo}")
    if addr not in CLIENTS:
        CLIENTS[addr] = {}
        CLIENTS[addr]["websocket"] = websocket
        CLIENTS[addr]["pseudo"] = pseudo
        await announce(f"{pseudo} has joined the chatroom")

    try:
        while True:
            msg = await websocket.recv()
            sender_pseudo = CLIENTS[addr]["pseudo"]
            formatted_msg = f"{Fore.BLUE}{sender_pseudo}:{Style.RESET_ALL} {msg}"
            print(formatted_msg)

            for client_addr, client_info in CLIENTS.items():
                if client_addr != addr:
                    await client_info["websocket"].send(formatted_msg)

            if addr in CLIENTS and "saluted" not in CLIENTS[addr]:
                await websocket.send('')
                CLIENTS[addr]["saluted"] = True

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection with {Fore.BLUE}{pseudo}{Style.RESET_ALL} closed")
        del CLIENTS[addr]


async def announce(announcement):
    for client_addr, client_info in CLIENTS.items():
        announcement = f"{Fore.GREEN}{announcement}{Style.RESET_ALL}"
        await client_info["websocket"].send(f"{Fore.RED}Announcement:{Style.RESET_ALL} {announcement}")


async def main():
    server = await websockets.serve(handle_client_msg, host, port)
    print(f'Serving on {server.sockets[0].getsockname()}')

    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
