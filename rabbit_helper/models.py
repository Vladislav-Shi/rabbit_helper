from pydantic import BaseModel


class BaseRabbitConfig(BaseModel):
    """Базовая модель для создания подключения"""
    url: str
    queue_name: str
