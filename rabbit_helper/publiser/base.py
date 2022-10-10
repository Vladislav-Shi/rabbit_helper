import logging
from typing import Union

from aio_pika import logger
from aio_pika.abc import AbstractQueue, AbstractExchange, ExchangeType

from rabbit_helper.base.connections import BaseConnection
from rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.models import BasePublisherConfig

logger.setLevel(logging.DEBUG)


class BaseAsyncPublisher:
    _connection: BaseConnection
    _exchange: AbstractExchange
    _queue: AbstractQueue
    _config: BasePublisherConfig

    def __init__(self, config: BasePublisherConfig):
        self._config = config

    async def declare_queue(self) -> None:
        self._exchange = await self._connection.get_channel().declare_exchange(
            self._config.exchange_name,
            ExchangeType.DIRECT,
            durable=True
        )
        self._queue = await self._connection.get_channel().declare_queue(self._config.queue_name, durable=True)
        await self._queue.bind(self._exchange, routing_key=self._config.queue_name)

    async def publish(self, message: Union[str, bytes, dict]):
        """если очередь отсутсвует попытается создать ее еще раз"""
        if not await self._connection.check(self._queue.name):
            logger.error('connection close! Try reopen')
            await self.declare_queue()
        await self._exchange.publish(RabbitMessage(message), routing_key=self._queue.name)
        logger.debug('message was pushed')

    @classmethod
    async def create_publisher(cls, config: BasePublisherConfig) -> 'BaseAsyncPublisher':
        """Создает из конфига базового публикатора"""
        logger.debug('create publisher')
        publisher = cls(config=config)
        publisher._connection = await BaseConnection.create_connection(config=config.connection)
        await publisher.declare_queue()
        return publisher
