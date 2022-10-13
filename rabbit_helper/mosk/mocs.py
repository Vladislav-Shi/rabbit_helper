from typing import Union
from unittest.mock import Mock

from ...rabbit_helper.models import BaseRabbitConfig


class PublisherMock:
    async def publish(self, message: Union[str, bytes, dict]):
        pass

    @classmethod
    async def create_consumer(cls, config: BaseRabbitConfig) -> 'BaseAsyncPublisher':
        return Mock()


class ConsumerMock:
    async def consume(self):
        pass

    @classmethod
    async def create_consumer(cls, config: BaseRabbitConfig):
        return Mock()
