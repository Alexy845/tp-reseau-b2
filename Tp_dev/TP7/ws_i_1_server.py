import asyncio
import websockets

async def hello(websocket):
    string = await websocket.recv()
    print(f"<<< {string}")
    greeting = f"Hello client ! Received {string}"
    await websocket.send(greeting)
    print(f">>> {greeting}")


async def main():
    async with websockets.serve(hello, "localhost", 8765):
        print("Server running...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
