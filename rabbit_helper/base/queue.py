from abc import ABC, abstractmethod


class AbstractQueue(ABC):
    queue_name: str

    @abstractmethod
    async def declare(self):
        pass

    @abstractmethod
    async def close(self):
        pass
