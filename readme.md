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

### Consumer с мертвой очередью
В проекте присутсвует класс `from rabbit_helper.consumer.consumers import Consumer`. Он обеспечивает более безопасную работу с сообщениями.
Все те сообщения которые по той или иной причине не были выполнены он помещает в 'мертвую очередь' где сообщения хранятся заданное время и потом пересылаются в основную очередь
(время задается в конфиге).

Пример:
```python
async def func(message: RabbitMessage):
    print('New message:', message.dict())
    msg = message.dict()
    if msg.get('crush'):
        print('error')
        raise ValueError('fail!')


async def main():
    config = ConsumerConfig(queue_name='test', message_ttl=10000)  # 10 секунд
    consumer = await Consumer.create_consumer(config=config)
    await consumer.set_perform(func)
    await consumer.consume()

if __name__ == '__main__':
    asyncio.run(main())
```