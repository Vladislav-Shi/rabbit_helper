from abc import ABC, abstractmethod

import aio_pika

from rabbit_helper.models import RabbtiConnectionConfig


class AbstractConnection(ABC):
    connection_url: str
    connection: aio_pika.connection.AbstractConnection
    channel: aio_pika.channel.AbstractChannel

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def check(self) -> bool:
        return False


class BaseConnection(AbstractConnection):
    _config: RabbtiConnectionConfig

    def __init__(self, config: RabbtiConnectionConfig):
        self._config = config

    async def connect(self):
        self.connection = await aio_pika.connect(
            host=self._config.host,
            port=self._config.port,
            login=self._config.login,
            password=self._config.password,
            virtualhost=self._config.virtualhost,
            ssl=self._config.ssl
        )
        self.channel = await self.connection.channel()

    async def check(self) -> bool:
        """Если подключение отсутсвует вернет False, если есть True"""
        if self.connection.is_closed:
            return False

    async def disconnect(self):
        await self.connection.close()

    def get_channel(self) -> aio_pika.channel.AbstractChannel:
        return self.channel

    @classmethod
    async def create_connection(cls, config: RabbtiConnectionConfig) -> 'BaseConndection':
        connection = cls(config=config)
        await connection.connect()
        return connection
