from abc import ABC, abstractmethod

import aio_pika


class AbstractConnection(ABC):
    connection_url: str
    connection: aio_pika.connection.AbstractConnection

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def check(self) -> bool:
        return False


class BaseConndection(AbstractConnection):

    def __init__(self, connection_url: str):
        self.connection_url = connection_url

    async def connect(self):
        self.connection = await aio_pika.connect(self.connection_url)

    async def check(self) -> bool:
        pass

    async def disconnect(self):
        await self.connection.close()

    @classmethod
    async def create_connection(cls, connection_url: str) -> 'BaseConndection':
        connection = cls(connection_url=connection_url)
        await connection.connect()
        return connection
