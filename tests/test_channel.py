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
    monkeypatch.setattr('rabbitmq_adapter.channel.pika', mocked_pika)

    rabbitmq_adapter.channel.create('MORTY HOST')

    mocked_pika.URLParameters.assert_called_once_with('MORTY HOST')

@pytest.mark.unit
def test_channel_creates_connection(monkeypatch):
    mocked_pika = Mock()
    mocked_pika.URLParameters.return_value = 'MORTY'
    mocked_pika.BlockingConnection.return_value = pika.Connection()
    monkeypatch.setattr('rabbitmq_adapter.channel.pika', mocked_pika)

    rabbitmq_adapter.channel.create('MORTY HOST')

    mocked_pika.BlockingConnection.assert_called_once_with('MORTY')
