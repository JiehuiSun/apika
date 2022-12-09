# -*- coding: utf-8 -*-


import asyncio
import json
from typing import Any

import aio_pika


class Apika(object):
    def __init__(self, *args, **kwargs):
        """Except for individual parameters, other parameters are consistent with <aio_pika.connect_robust>"""
        self.args: tuple = args
        self.kwargs: dict = kwargs

        self.is_inited: bool = False
        self.stop: bool = False
        self.channel: aio_pika.abc.AbstractRobustConnection = None
        self.connection: aio_pika.RobustConnection = None

        self.wait_time: [int, float] = self.kwargs.get("wait_time", 0)
        self.no_ack: bool = self.kwargs.get("no_ack", True)
        self.queue_name: str = self.kwargs.get("queue_name", "default_queue")
        self.exchange: str = self.kwargs.get("exchange", "")

    async def init_app(self):
        for k, v in self.kwargs.items():
            setattr(self, k, v)

        self.connection: aio_pika.RobustConnection = await aio_pika.connect_robust(*self.args, **self.kwargs)

        self.channel: aio_pika.abc.AbstractChannel = await self.connection.channel()
        if self.exchange:
            self.exchange: aio_pika.abc.AbstractExchange = await self.channel.declare_exchange(self.exchange)

        self.is_inited = True

        return self

    async def push(self, data: Any, *args, **kwargs):
        """
        Push Data

        :params data: Data
        """
        if not self.is_inited:
            raise SystemError("Need object.init_app()")

        if self.exchange:
            obj = self.exchange
        else:
            obj = self.channel.default_exchange

        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data).encode()
        else:
            data = str(data).encode()
        await obj.publish(
            aio_pika.Message(
                body=data
            ),
            routing_key=self.kwargs.get("routing_key", self.queue_name)
        )

    async def get(self,
                  callback,
                  params: [tuple, list] = (),
                  wait_time: [int, float] = 0,
                  *args, **kwargs):
        """
        Queue Data

        :params callback: callback async func
        :params params: a tuple or list, callback params
        :params wait_time: get a data, sleep time
        :params stop: while stop
        """
        if not self.is_inited:
            raise SystemError("Need object.init_app()")

        queue: aio_pika.abc.AbstractQueue = await self.channel.declare_queue(
            self.queue_name,
            # auto_delete=True,
            # exclusive=True
        )

        if self.exchange:
            await queue.bind(self.exchange)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        data = json.loads(message.body)
                    except json.decoder.JSONDecodeError:
                        data = message.body.decode()
                    await callback(data, *params)
                await asyncio.sleep(self.wait_time)

    async def __aenter__(self):
        return await self.init_app()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.connection.close()
