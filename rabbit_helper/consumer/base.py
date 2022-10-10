import asyncio
from typing import Callable

from aio_pika.abc import AbstractQueue

from rabbit_helper.base.connections import BaseConnection
from rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.models import BaseConsumerConfig


class BaseAsyncConsumer:
    _connection: BaseConnection
    _queue: AbstractQueue
    _config: BaseConsumerConfig

    def __init__(self, config: BaseConsumerConfig):
        self._config = config

    async def _perform(self, message: RabbitMessage):
        """Метод логики обработки после получения"""
        pass

    async def consume(self):
        async for message in self._queue:
            await self._perform(RabbitMessage.from_message(message))
            await message.ack()

    def __del__(self):
        self._connection.disconnect()

    async def set_perform(self, func: Callable[[RabbitMessage], None]) -> None:
        """
        :param func: функция типа async def func(message: RabbitMessage) -> None:
        """
        self._perform = func

    @classmethod
    async def create_consumer(cls, config: BaseConsumerConfig) -> 'BaseAsyncConsumer':
        """Создает из конфига базового слушателя"""
        print('Create consumer start')
        consumer = cls(config=config)
        consumer._connection = await BaseConnection.create_connection(config=config.connection)
        consumer._queue = await consumer._connection.get_channel().declare_queue(config.queue_name,  durable=True)
        return consumer
