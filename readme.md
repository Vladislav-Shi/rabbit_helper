##Скрипт надстрйока для работы с RabbitMq
Данная библиотека служит для упрощенного создания publisher и consumer которые работают с RabbitMq. Основано на библиотеке aoi_pika.

### Базовое использование
Набор слушателей для готового использования.\
Код базового использвоания слушателя
```python
    async def func(message: RabbitMessage):
        print('New message:', message.payload)
        
    config = BaseConsumerConfig(queue_name='test')
    consumer = await BaseAsyncConsumer.create_consumer(config=config)
    await consumer.set_perfome(func)
    await consumer.consume()
```
Пример базового использвоания паблишера
```python
    config = BasePublisherConfig(queue_name='test')
    publisher = await BaseAsyncPublisher.create_consumer(config=config)
    await publisher.publish(message={'hello': 'world'})
```
Данные классы отправляют и обрабатывают сообщения в формате json. Иные форматы вызывают исключение