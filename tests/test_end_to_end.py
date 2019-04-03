import pytest
import rabbitmq_adapter
import sys
import os

sys.path.append(os.environ['CONFIG'])
from config import *

def setup_listener(
    channel,
    on_message_callback,
    queue=config.rabbitmq.queue,
    exchange=config.rabbitmq.exchange,
    durable=False,
    prefetch_count=config.rabbitmq.prefetch.count
):
    channel.queue_declare(queue=queue, durable=durable)
    channel.queue_bind(queue=queue, exchange=exchange)
    channel.basic_qos(prefetch_count=prefetch_count)
    channel.basic_consume(queue=queue, on_message_callback=on_message_callback)

    return channel

@pytest.mark.only
def test_rabbitmq_factory():
    # Should be able to create a RabbitMQ connection
    called = False
    def mocked_handler(ch, method, props, body):
        called = True
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.close()

        assert called

    rabbitmq_channel = rabbitmq_adapter.channel.create(config.rabbitmq.host)
    rabbitmq_channel = setup_listener(rabbitmq_channel, mocked_handler)
    rabbitmq_channel.basic_publish(
        exchange=config.rabbitmq.exchange,
        routing_key=config.rabbitmq.queue,
        body='MORTY'
    )

    rabbitmq_channel.start_consuming()

def test_rabbitmq_listen_to_queue():
    # Should be able to listen to a RabbitMQ queue
    assert True

def test_rabbitmq_queue_one_to_many_queue_handler():
    # Should be able to have an one-to-many relationship between the queue and the handler function
    assert True

def test_rabbitmq_send_message():
    # Should be able to send a message in a given queue
    assert True
