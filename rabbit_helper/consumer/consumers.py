from aio_pika.abc import AbstractQueue

from rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.consumer.base import BaseAsyncConsumer
from rabbit_helper.models import BaseConsumerConfig


class Consumer(BaseAsyncConsumer):
    _dead_queue: AbstractQueue
    """
    Этот слушатель в случай если задача не была выполнена помещает в очередь мертвых сообщений.
    """
    async def consume(self):
        async for message in self._queue:
            try:
                await self._perform(RabbitMessage.from_message(message))
                await message.ack()
            except Exception:
                await message.ack()
                await self._connection.get_channel().default_exchange.publish(
                    message,
                    routing_key=self._dead_queue.name)

    def get_dq_name(self):
        return f"{self._config.queue_name}_DQ"

    @classmethod
    async def create_consumer(cls, config: BaseConsumerConfig) -> 'Consumer':
        """Создает из конфига базового слушателя"""
        consumer: Consumer = await super().create_consumer(config=config)
        consumer._dead_queue = await consumer._connection.get_channel().declare_queue(
            consumer.get_dq_name(),
            auto_delete=False,
            durable=True,
            arguments={'x-queue-mode': 'lazy'}
        )
        return consumer
