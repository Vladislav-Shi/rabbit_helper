import asyncio
from typing import Callable

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue

from rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.models import BaseRabbitConfig


class BaseAsyncConsumer:
    _connection: AbstractConnection
    _queue: AbstractQueue
    _channel: AbstractChannel

    async def perfome(self, message: RabbitMessage):
        """Метод логики обработки после получения"""
        pass

    async def consume(self):
        async for message in self._queue:
            await self.perfome(RabbitMessage.from_message(message))

    def __del__(self):
        self._connection.close()

    async def set_perfome(self, func: Callable[[RabbitMessage], None]):
        self.perfome = func

    @classmethod
    async def create_consumer(cls, config: BaseRabbitConfig) -> 'BaseAsyncConsumer':
        """Создает из конфига базового слушателя"""
        print('Create consumer start')
        consumer = cls()
        consumer._connection = await aio_pika.connect(url=config.url)
        consumer._channel = await consumer._connection.channel()
        consumer._queue = await consumer._channel.declare_queue(config.queue_name, auto_delete=True)
        return consumer


async def func(message: RabbitMessage):
    print('New message:', message.payload)
    print('New message:', message.dict())

async def main():
    config = BaseRabbitConfig(queue_name='test', url='amqp://guest:guest@127.0.0.1/')
    consumer = await BaseAsyncConsumer.create_consumer(config=config)
    await consumer.set_perfome(func)
    await consumer.consume()

if __name__ == '__main__':
    asyncio.run(main())