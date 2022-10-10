import json
import logging
from typing import Union

from aio_pika import Message


class RabbitMessage(Message):
    """Класс надстройка над стандартнрым aio_pika.
    Нужен чтобы удобнее было отправлять и получать данные с сообщения
    В качестве сообщений служат json"""
    payload: Union[str, bytes, dict]

    @classmethod
    def from_message(cls, message: Message):
        return cls(payload=message.body)

    def __init__(self, payload: Union[str, bytes, dict]):
        if isinstance(payload, bytes):
            super().__init__(body=payload)
        elif isinstance(payload, str):
            super().__init__(body=payload.encode())
        else:
            super(RabbitMessage, self).__init__(body=json.dumps(payload).encode())
        self.payload = payload

    def dict(self):
        try:
            if isinstance(self.payload, dict):
                return self.payload
            else:
                return json.loads(self.payload)
        except Exception:
            logging.debug('Message must be correct JSON')
