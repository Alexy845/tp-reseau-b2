import asyncio
import aioconsole
from colorama import Fore, Style
import sys
import websockets
host = '127.0.0.1'
port = 8888

async def send_username(websocket):
    username = input(f"{Fore.RED}Enter your username: {Style.RESET_ALL}")
    user = f"Hello|{username}"
    await websocket.send(user)

async def receive_messages(websocket):
    async for data in websocket:
        if data == '':
            print(f"{Fore.RED}Disconnected from the server{Style.RESET_ALL}")
            sys.exit()
            
        print(data)

async def user_input(websocket):
    while True:
        message = await aioconsole.ainput("")
        await websocket.send(message)
        await asyncio.sleep(0.1)

async def main():
    uri = f"ws://{host}:{port}"
    async with websockets.connect(uri) as websocket:
        await send_username(websocket)

        input_task = asyncio.ensure_future(user_input(websocket))
        receive_task = asyncio.ensure_future(receive_messages(websocket))

        await asyncio.gather(input_task, receive_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
