import asyncio

async def p1():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.5)


loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(p1()),
    loop.create_task(p1()),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()