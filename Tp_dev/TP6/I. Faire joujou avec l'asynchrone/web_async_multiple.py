import asyncio
import aiohttp
import aiofiles
import os

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def write_content(content, file):
    async with aiofiles.open(file, 'w') as f:
        await f.write(content)
        print(f"Content written to {file} successfully.")

async def process_urls_from_file(file_path):
    async with aiofiles.open(file_path, 'r') as f:
        urls = await f.readlines()
        tasks = []
        for url in urls:
            url = url.strip()  
            url = url.replace('https://', '')  
            file_name = url.replace('/', '_')
            content = await get_content(url)
            if content:
                file_path = f"/tmp/web_{file_name}"
                tasks.append(write_content(content, file_path))
        await asyncio.gather(*tasks)

async def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python web_async_multiple.py <file_with_urls>")
        sys.exit(1)

    urls_file = sys.argv[1]
    if not os.path.isfile(urls_file):
        print(f"File '{urls_file}' not found.")
        sys.exit(1)

    await process_urls_from_file(urls_file)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
