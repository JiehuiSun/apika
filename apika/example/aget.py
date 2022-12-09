# -*- coding: utf-8 -*-


import time
import asyncio
from apika import Apika


async def __callback(data, *args, **kwargs):
    print(f"Msg is {data}")


async def test_get(loop):
    """Mode 1"""
    a = Apika(loop=loop)
    await a.init_app()
    await a.get(__callback, (time.time(),))


async def test_get2(loop):
    """Mode 2"""
    async with Apika(loop=loop) as a:
        await a.get(__callback, (time.time(),))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_get(loop))
    loop.run_until_complete(test_get2(loop))
    loop.close()
