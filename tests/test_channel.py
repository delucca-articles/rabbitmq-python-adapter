import pytest
import rabbitmq_adapter
import sys
import os
from unittest.mock import Mock
from tests.__mocks__ import pika

sys.path.append(os.environ['CONFIG'])
from config import *

@pytest.mark.unit
def test_channel_sets_parameters(monkeypatch):
    mocked_pika = Mock()
    mocked_pika.URLParameters.return_value = 'MORTY'
    mocked_pika.BlockingConnection.return_value = pika.Connection()
    monkeypatch.setattr('rabbitmq_adapter.channel.pika', mocked_pika)

    Channel = rabbitmq_adapter.channel.create('MORTY HOST')

    mocked_pika.URLParameters.assert_called_once_with('MORTY HOST')

@pytest.mark.unit
def test_channel_creates_connection(monkeypatch):
    mocked_pika = Mock()
    mocked_pika.URLParameters.return_value = 'MORTY'
    mocked_pika.BlockingConnection.return_value = pika.Connection()
    monkeypatch.setattr('rabbitmq_adapter.channel.pika', mocked_pika)

    Channel = rabbitmq_adapter.channel.create('MORTY HOST')

    mocked_pika.BlockingConnection.assert_called_once_with('MORTY')

@pytest.mark.integration
def test_channel(monkeypatch):
    Channel = rabbitmq_adapter.channel.create(config.rabbitmq.host)

    assert 'exchange_declare' in dir(Channel)
    assert 'queue_declare'   in dir(Channel)
    assert 'queue_bind' in dir(Channel)
    assert 'basic_qos' in dir(Channel)
    assert 'basic_consume' in dir(Channel)
    assert 'start_consuming' in dir(Channel)
    assert 'basic_publish' in dir(Channel)
