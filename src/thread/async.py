import asyncio


# this a worst way beacuase iterators block main thread
async def a():
    for i in range(1, 10):
        print(f'hello world def a {i}')
        await asyncio.sleep(1)

async def b():
    for i in range(1, 10):
        print(f'hello world def b {i}')
        await asyncio.sleep(1)

asyncio.run(a())
asyncio.run(b())
