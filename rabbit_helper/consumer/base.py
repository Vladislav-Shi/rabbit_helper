import logging
from typing import Callable

from aio_pika import logger
from aio_pika.abc import AbstractQueue, ExchangeType, AbstractExchange

from ...rabbit_helper.base.connections import BaseConnection
from ...rabbit_helper.base.mesage import RabbitMessage
from ...rabbit_helper.models import BaseConsumerConfig

logger.setLevel(logging.DEBUG)


class BaseAsyncConsumer:
    _connection: BaseConnection
    _exchange: AbstractExchange
    _queue: AbstractQueue
    _config: BaseConsumerConfig

    def __init__(self, config: BaseConsumerConfig):
        self._config = config

    async def declare_queue(self) -> None:
        self._exchange = await self._connection.get_channel().declare_exchange(
            self._config.exchange_name,
            ExchangeType.DIRECT,
            durable=True
        )
        self._queue = await self._connection.get_channel().declare_queue(self._config.queue_name, durable=True)
        await self._queue.bind(self._exchange, routing_key=self._config.queue_name)

    async def perform(self, message: RabbitMessage):
        """Метод логики обработки после получения"""
        pass

    async def consume(self):
        logger.info('Consume message')
        async for message in self._queue:
            await self.perform(RabbitMessage.from_message(message))
            await message.ack()
    #
    # def __del__(self):
    #     self._connection.disconnect()

    async def set_perform(self, func: Callable[[RabbitMessage], None]) -> None:
        """
        :param func: функция типа async def func(message: RabbitMessage) -> None:
        """
        self.perform = func

    @classmethod
    async def create_consumer(cls, config: BaseConsumerConfig) -> 'BaseAsyncConsumer':
        """Создает из конфига базового слушателя"""
        logger.debug('Create consumer start')
        consumer = cls(config=config)
        consumer._connection = await BaseConnection.create_connection(config=config.connection)
        await consumer.declare_queue()
        return consumer
