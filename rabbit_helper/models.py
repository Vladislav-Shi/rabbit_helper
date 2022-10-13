from pydantic import BaseModel


class RabbtiConnectionConfig(BaseModel):
    """Модель для подключения к rabbit"""
    host: str = 'localhost'
    port: int = 5672
    login: str = 'guest'
    password: str = 'guest'
    virtualhost: str = '/'
    ssl: bool = False


class BasePublisherConfig(BaseModel):
    exchange_name: str = 'basic_exchange'
    connection: RabbtiConnectionConfig = RabbtiConnectionConfig()
    queue_name: str


class BaseConsumerConfig(BaseModel):
    exchange_name: str = 'basic_exchange'
    connection: RabbtiConnectionConfig = RabbtiConnectionConfig()
    durable_queue: bool = False  # долговечность очереди
    queue_name: str


class ConsumerConfig(BaseConsumerConfig):
    message_ttl: int = 600000  # по-умолчанию пусть живет 10 минут


class BaseRabbitConfig(BaseModel):
    """Базовая модель для создания подключения"""
    url: str
    queue_name: str
