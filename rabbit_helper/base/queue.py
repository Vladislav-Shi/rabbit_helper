from abc import ABC, abstractmethod

import aio_pika

connection = await aio_pika.connect(
    "amqp://guest:guest@127.0.0.1/",
)

queue_name = "test_queue"

# Creating channel
channel = await connection.channel()
aio_pika.Message

# Maximum message count which will be processing at the same time.
await channel.set_qos(prefetch_count=100)

# Declaring queue
queue = await channel.declare_queue(queue_name, auto_delete=True)


class AbstractQueue(ABC):
    queue_name: str

    @abstractmethod
    async def declare(self):
        pass

    @abstractmethod
    async def close(self):
        pass
