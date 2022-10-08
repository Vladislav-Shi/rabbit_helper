import asyncio
from typing import Union

from aio_pika.abc import AbstractQueue

from rabbit_helper.base.connections import BaseConnection
from rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.models import BasePublisherConfig


class BaseAsyncPublisher:
    _connection: BaseConnection
    _queue: AbstractQueue
    _config: BasePublisherConfig

    def __init__(self, config: BasePublisherConfig):
        self._config = config

    async def publish(self, message: Union[str, bytes, dict]):
        """если очередь отсутсвует попытается создать ее еще раз"""
        if not await self._connection.check(self._queue.name):
            self._queue = await self._connection.get_channel().declare_queue(
                self._config.queue_name,
                auto_delete=True
            )
        await self._connection.get_channel().default_exchange.publish(
            RabbitMessage(message),
            routing_key=self._queue.name)

    @classmethod
    async def create_consumer(cls, config: BasePublisherConfig) -> 'BaseAsyncPublisher':
        """Создает из конфига базового публикатора"""
        publisher = cls(config=config)
        publisher._connection = await BaseConnection.create_connection(config=config.connection)
        publisher._queue = await publisher._connection.get_channel().declare_queue(config.queue_name, auto_delete=True)
        return publisher


async def main():
    config = BasePublisherConfig(queue_name='test')
    publisher = await BaseAsyncPublisher.create_consumer(config=config)
    # await asyncio.sleep(10)
    await publisher.publish(message={'hello': 'world'})


if __name__ == "__main__":
    asyncio.run(main())
