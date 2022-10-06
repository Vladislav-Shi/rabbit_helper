import asyncio


def run_worker():
    """Запускает асинхронно воркер"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete()
