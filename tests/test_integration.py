import pytest
import rabbitmq_adapter
import sys
import os
from time import sleep

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

def wait_for_result(
    anchor,
    expected,
    tries=0,
    retry_after=.6
):
    if anchor == expected or tries > 5: assert anchor == expected
    else:
        sleep(retry_after)
        return wait_for_result(anchor, expected, tries + 1)

@pytest.mark.integration
def test_rabbitmq_factory():
    # Should be able to create a RabbitMQ connection
    calls = []
    expected = [1]

    def mocked_handler(ch, method, props, body):
        calls.append(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.close()

    rabbitmq_channel = rabbitmq_adapter.channel.create(config.rabbitmq.host)
    rabbitmq_channel = setup_listener(rabbitmq_channel, mocked_handler)
    rabbitmq_channel.basic_publish(
        exchange=config.rabbitmq.exchange,
        routing_key=config.rabbitmq.queue,
        body='MORTY'
    )

    rabbitmq_channel.start_consuming()
    wait_for_result(calls, expected)

@pytest.mark.integration
def test_rabbitmq_listen_to_queue():
    # Should be able to listen to a RabbitMQ queue
    calls = []
    expected = [1]
    rabbitmq_channel = rabbitmq_adapter.channel.create(config.rabbitmq.host)

    def mocked_handler(ch, method, props, body):
        calls.append(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.close()

    rabbitmq_adapter.subscriber.subscribe(rabbitmq_channel, mocked_handler, durable=False)
    rabbitmq_channel.basic_publish(
        exchange=config.rabbitmq.exchange,
        routing_key=config.rabbitmq.queue,
        body='MORTY'
    )

    rabbitmq_channel.start_consuming()
    wait_for_result(calls, expected)

@pytest.mark.integration
def test_rabbitmq_queue_one_to_many_queue_handler():
    # Should be able to have an one-to-many relationship between the queue and the handler function
    calls = []
    expected = [1, 1]
    second_queue = 'TEST::NEW_2'
    rabbitmq_channel = rabbitmq_adapter.channel.create(config.rabbitmq.host)

    def mocked_handler(ch, method, props, body):
        calls.append(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        if calls == expected: ch.close()

    rabbitmq_adapter.subscriber.subscribe(rabbitmq_channel, mocked_handler, durable=False)
    rabbitmq_adapter.subscriber.subscribe(rabbitmq_channel, mocked_handler, durable=False, queue=second_queue)
    rabbitmq_channel.basic_publish(
        exchange=config.rabbitmq.exchange,
        routing_key=config.rabbitmq.queue,
        body='MORTY'
    )
    rabbitmq_channel.basic_publish(
        exchange=config.rabbitmq.exchange,
        routing_key=second_queue,
        body='MORTY'
    )

    rabbitmq_channel.start_consuming()
    wait_for_result(calls, expected)

def test_rabbitmq_send_message():
    # Should be able to send a message in a given queue
    assert True
