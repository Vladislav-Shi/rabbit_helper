import asyncio
from typing import Union

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractQueue, AbstractChannel

from rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.models import BaseRabbitConfig


class BaseAsyncPublisher:
    _connection: AbstractConnection
    _queue: AbstractQueue
    _channel: AbstractChannel

    async def publish(self, message: Union[str, bytes, dict]):
        await self._channel.default_exchange.publish(
            RabbitMessage(message),
            routing_key=self._queue.name)

    @classmethod
    async def create_consumer(cls, config: BaseRabbitConfig) -> 'BaseAsyncPublisher':
        """Создает из конфига базового публикатора"""
        publisher = cls()
        publisher._connection = await aio_pika.connect(url=config.url)
        publisher._channel = await publisher._connection.channel()
        publisher._queue = await publisher._channel.declare_queue(config.queue_name, auto_delete=True)
        return publisher


async def main():
    config = BaseRabbitConfig(queue_name='test', url='amqp://guest:guest@127.0.0.1/')
    publisher = await BaseAsyncPublisher.create_consumer(config=config)
    await publisher.publish(message={'hello': 'world'})


if __name__ == "__main__":
    asyncio.run(main())
