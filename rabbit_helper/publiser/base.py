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
        publisher._queue = await publisher._connection.get_channel().declare_queue(config.queue_name, durable=True)
        return publisher


class SingletonAsyncPublisher(BaseAsyncPublisher):
    """Singleton версия паблишера
    Хранит по одному экземпляру для каждой очереди"""
    _instance = dict()

    def __init__(self, queue_name):
        pass

    def __new__(cls, queue_name: str = 'main'):
        if queue_name not in cls._instance:
            cls._instance[queue_name] = super().__new__(cls)
            cls._instance[queue_name]._config = None
            cls._instance[queue_name]._connection = None
            cls._instance[queue_name]._queue = None
        return cls._instance[queue_name]

    async def create_consumer(self, config: BasePublisherConfig):
        self._config = config
        self._connection = await BaseConnection.create_connection(config=self._config.connection)
        self._queue = await self._connection.get_channel().declare_queue(self._config.queue_name, durable=True)
