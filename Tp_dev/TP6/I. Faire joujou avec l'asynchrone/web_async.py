import asyncio
import aiohttp
import aiofiles


async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def write_content(content, file):
    async with aiofiles.open(file, 'w') as f:
        await f.write(content)
        print(f"Content written to {file} successfully.")

async def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python web_async.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = await get_content(url)
    if content:
        await write_content(content, '/tmp/web_page')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()