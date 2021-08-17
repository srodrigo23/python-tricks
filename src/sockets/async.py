import asyncio

async def a():
    print('hello')
    await asyncio.sleep(1)
    print('world')

async def b():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(a())
asyncio.run(b())