##Скрипт надстрйока для работы с RabbitMq
Данная библиотека служит для упрощенного создания publisher и consumer которые работают с RabbitMq. Основано на библиотеке aoi_pika.

### Consumer
Набор слушателей для готового использования.\
Код базового использвоания слушателя
```python
    async def func(message: RabbitMessage):
        print('New message:', message.payload)
        
    config = BaseRabbitConfig(queue_name='test', url='amqp://guest:guest@127.0.0.1/')
    consumer = await BaseAsyncConsumer.create_consumer(config=config)
    await consumer.set_perfome(func)
    await consumer.consume()
```
