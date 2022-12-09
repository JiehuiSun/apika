# -*- coding: utf-8 -*-


import time
import asyncio
from apika import Apika


async def test_push(loop):
    """Mode 1"""
    a = Apika(loop=loop)
    await a.init_app()
    for i in range(10):
        await a.push(f"This is msg {i}")
    await a.connection.close()


async def test_push2(loop):
    """Mode 2"""
    async with Apika(loop=loop) as a:
        for i in range(10):
            await a.push({"id": i})


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_push(loop))
    loop.run_until_complete(test_push2(loop))
    loop.close()
