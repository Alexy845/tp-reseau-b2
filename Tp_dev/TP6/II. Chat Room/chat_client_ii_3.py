import asyncio
import aioconsole

host = '127.0.0.1'
port = 8888

async def receive_messages(reader):
    while True:
        data = await reader.read(1024)
        if data == b'':
            break
        print(data.decode())

async def user_input(writer):
    while True:
        message = await aioconsole.ainput("")
        writer.write(message.encode())
        await writer.drain()
        await asyncio.sleep(0.1)

async def main():

    reader, writer = await asyncio.open_connection(host, port)

    task_receive = asyncio.create_task(receive_messages(reader))
    task_input = asyncio.create_task(user_input(writer))

    await asyncio.gather(task_receive, task_input)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
