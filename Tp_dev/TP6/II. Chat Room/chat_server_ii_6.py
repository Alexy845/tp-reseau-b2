import asyncio
from colorama import Fore, Style

host = '127.0.0.1'
port = 8888
global CLIENTS
CLIENTS = {}


async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New client: {addr[0]}:{addr[1]}")

    data = await reader.read(1024)
    message = data.decode()

    pseudo = message.split("|")[1]
    print(f"{addr[0]}:{addr[1]} has chosen the pseudo {pseudo}")
    if addr not in CLIENTS:
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        CLIENTS[addr]["pseudo"] = pseudo
        await announce(f"{pseudo} has joined the chatroom")

    while True:
        data = await reader.read(1024)
        if data == b'':
            break

        msg = data.decode()
        sender_pseudo = CLIENTS[addr]["pseudo"]
        formatted_msg = f"{Fore.BLUE}{sender_pseudo}:{Style.RESET_ALL} {msg}"
        print(formatted_msg)

        for client_addr, client_info in CLIENTS.items():
            if client_addr != addr:
                client_info["w"].write(formatted_msg.encode())
                await client_info["w"].drain()

        if addr in CLIENTS and "saluted" not in CLIENTS[addr]:
            await writer.drain()
            CLIENTS[addr]["saluted"] = True

    print(f"Connection with {Fore.BLUE}{pseudo}{Style.RESET_ALL} closed")
    writer.close()


async def announce(announcement):
    for client_addr, client_info in CLIENTS.items():
        announcement = f"{Fore.GREEN}{announcement}{Style.RESET_ALL}"
        client_info["w"].write(f"{Fore.RED}Announcement:{Style.RESET_ALL} {announcement}".encode())
        await client_info["w"].drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, host, port)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    asyncio.run(main())
