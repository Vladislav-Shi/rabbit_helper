from aio_pika import ExchangeType
from pydantic import BaseModel


class RabbtiConnectionConfig(BaseModel):
    """Модель для подключения к rabbit"""
    host: str = 'localhost'
    port: int = 5672
    login: str = 'guest'
    password: str = 'guest'
    virtualhost: str = '/'
    ssl: bool = False


class ExchangeConfig(BaseModel):
    exchange_type: ExchangeType = ExchangeType.DIRECT
    durable_queue: bool = False  # долговечность очереди
    auto_delete: bool = True  # Автоматически удалять очередь


class BasePublisherConfig(BaseModel):
    connection: RabbtiConnectionConfig = RabbtiConnectionConfig()
    queue_name: str


class BaseConsumerConfig(BaseModel):
    connection: RabbtiConnectionConfig = RabbtiConnectionConfig()
    durable_queue: bool = False  # долговечность очереди
    queue_name: str


class BaseRabbitConfig(BaseModel):
    """Базовая модель для создания подключения"""
    url: str
    queue_name: str
