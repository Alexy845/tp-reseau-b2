import asyncio
import aioconsole
from colorama import Fore, Style
import sys

host = '127.0.0.1'
port = 8888

async def send_username(writer):
    username = input(f"{Fore.RED}Enter your username: {Style.RESET_ALL}")
    user = f"Hello|{username}"
    writer.write(user.encode())
    await writer.drain()

async def receive_messages(reader):
    while True:
        data = await reader.read(1024)
        if data == b'':
            print(f"{Fore.RED}Disconnected from the server{Style.RESET_ALL}")
            sys.exit()
            
        print(data.decode())

async def user_input(writer):
    while True:
        message = await aioconsole.ainput("")
        writer.write(message.encode())
        await writer.drain()
        await asyncio.sleep(0.1)

async def main():

    reader, writer = await asyncio.open_connection(host, port)

    await send_username(writer)

    input_task = asyncio.ensure_future(user_input(writer))
    receive_task = asyncio.ensure_future(receive_messages(reader))

    await asyncio.gather(input_task, receive_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
