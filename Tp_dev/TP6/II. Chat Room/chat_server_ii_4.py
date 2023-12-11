import asyncio

host = '127.0.0.1'
port = 8888
global CLIENTS
CLIENTS = {}
async def handle_client_msg(reader, writer):
    addr = writer.get_extra_info('peername')
    if addr not in CLIENTS:
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        print(f"New client connected: {addr}")
    
    writer.write(f"Hello {addr[0]}:{addr[1]}".encode())

    while True:
        data = await reader.read(1024)
        if data == b'':
            break
        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]}: {message}")

        for client_addr, client_info in CLIENTS.items():
            if client_addr != addr:
                msg_to_send = f"{host}:{port}: {message}"
                client_info["w"].write(msg_to_send.encode())
                await client_info["w"].drain()
        
        if addr in CLIENTS and "saluted" not in CLIENTS[addr]:
            await writer.drain()
            CLIENTS[addr]["saluted"] = True

    print(f"Connection with {addr[0]}:{addr[1]} closed")
    writer.close()

async def main():

    server = await asyncio.start_server(handle_client_msg, host, port)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
