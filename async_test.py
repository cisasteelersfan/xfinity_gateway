import asyncio
import aiohttp

async def get():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://10.0.0.1') as resp:
            print(resp.status)
            print(await resp.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(get()))