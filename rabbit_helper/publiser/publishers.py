from aio_pika.patterns import RPC

from ...rabbit_helper.models import BasePublisherConfig
from ...rabbit_helper.publiser.base import BaseAsyncPublisher


class RpcPublisher(BaseAsyncPublisher):
    rpc: RPC

    async def publish(self, message: dict) -> dict:
        """если очередь отсутсвует попытается создать ее еще раз"""
        if not await self._connection.check(self._queue.name):
            await self.declare_queue()
            self.rpc = await RPC.create(self._connection.get_channel())
        return await self.rpc.call("perform", kwargs={'message': message})

    @classmethod
    async def create_publisher(cls, config: BasePublisherConfig) -> 'RpcPublisher':
        publisher: RpcPublisher = await super().create_publisher(config=config)
        publisher.rpc = await RPC.create(publisher._connection.get_channel())
        return publisher

