from aio_pika.abc import AbstractQueue

from rabbit_helper.rabbit_helper.base.mesage import RabbitMessage
from rabbit_helper.rabbit_helper.consumer.base import BaseAsyncConsumer
from rabbit_helper.rabbit_helper.models import ConsumerConfig


class Consumer(BaseAsyncConsumer):
    _dead_queue: AbstractQueue
    _config: ConsumerConfig
    """
    Этот слушатель в случай если задача не была выполнена помещает в очередь мертвых сообщений.
    """

    async def declare_queue(self) -> None:
        await super().declare_queue()
        self._dead_queue = await self._connection.get_channel().declare_queue(
            self.get_dq_name(),
            auto_delete=False,
            durable=True,
            arguments={
                'x-queue-mode': 'lazy',
                'x-dead-letter-exchange': self._config.exchange_name,
                'x-dead-letter-routing-key': self._config.queue_name,
                'x-message-ttl': self._config.message_ttl
            }
        )
        await self._dead_queue.bind(self._exchange, routing_key=self.get_dq_name())

    async def consume(self):
        async for message in self._queue:
            try:
                await self.perform(RabbitMessage.from_message(message))
                await message.ack()
            except Exception:
                await self._exchange.publish(message, routing_key=self._dead_queue.name)
                await message.ack()

    def get_dq_name(self):
        return f"{self._config.queue_name}_DQ"

    @classmethod
    async def create_consumer(cls, config: ConsumerConfig) -> 'Consumer':
        """Создает из конфига базового слушателя"""
        consumer: Consumer = await super().create_consumer(config=config)
        return consumer