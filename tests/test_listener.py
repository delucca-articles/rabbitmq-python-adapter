import pytest
import rabbitmq_adapter
import sys
import os
from unittest.mock import Mock
from tests.__mocks__ import pika

sys.path.append(os.environ['CONFIG'])
from config import *

def mocked_handler(): pass

@pytest.mark.unit
def test_listener_queue_declared(monkeypatch):
    channel = pika.Channel()
    channel.queue_declare = Mock()

    rabbitmq_adapter.listener.subscribe(channel, mocked_handler)

    channel.queue_declare.assert_called_once_with(
        queue=config.rabbitmq.queue,
        durable=True
    )

@pytest.mark.unit
def test_listener_queue_bind(monkeypatch):
    channel = pika.Channel()
    channel.queue_bind = Mock()

    rabbitmq_adapter.listener.subscribe(channel, mocked_handler)

    channel.queue_bind.assert_called_once_with(
        queue=config.rabbitmq.queue,
        exchange=config.rabbitmq.exchange
    )

@pytest.mark.unit
def test_listener_basic_qos(monkeypatch):
    channel = pika.Channel()
    channel.basic_qos = Mock()

    rabbitmq_adapter.listener.subscribe(channel, mocked_handler)

    channel.basic_qos.assert_called_once_with(prefetch_count=config.rabbitmq.prefetch.count)

@pytest.mark.unit
def test_listener_basic_consume(monkeypatch):
    channel = pika.Channel()
    channel.basic_consume = Mock()

    rabbitmq_adapter.listener.subscribe(channel, mocked_handler)

    channel.basic_consume.assert_called_once_with(
        queue=config.rabbitmq.queue,
        on_message_callback=mocked_handler
    )
