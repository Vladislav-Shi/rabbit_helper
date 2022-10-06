from abc import ABC, abstractmethod

import aio_pika


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

    def __init__(self, connection_url: str):
        self.connection_url = connection_url

    async def connect(self):
        self.connection = await aio_pika.connect(self.connection_url)
        self.channel = await self.connection.channel()

    async def check(self) -> bool:
        """Если подключение отсутсвует вернет False, если есть True"""
        if self.connection.is_closed:
            return False
        return True

    async def disconnect(self):
        await self.connection.close()

    def get_channel(self) -> aio_pika.channel.AbstractChannel:
        return self.channel

    @classmethod
    async def create_connection(cls, connection_url: str) -> 'BaseConndection':
        connection = cls(connection_url=connection_url)
        await connection.connect()
        return connection
