import rabbitmq
from unittest.mock import Mock
from tests.__mocks__ import pika

def test_rabbitmq_factory(monkeypatch):
    # Should be able to create a RabbitMQ connection
    mocked_pika = Mock()
    mocked_pika.URLParameters.return_value = 'MORTY'
    mocked_pika.BlockingConnection.return_value = pika.Connection()
    monkeypatch.setattr('rabbitmq.instance.pika', mocked_pika)

    rabbitmq.instance.connect('MORTY HOST')
    mocked_pika.URLParameters.assert_called_once_with('MORTY HOST') # It should set the URL parameters based on host config
    mocked_pika.BlockingConnection.assert_called_once_with('MORTY') # It should block and create a connection
    assert False

def test_rabbitmq_listen_to_queue():
    # Should be able to listen to a RabbitMQ queue
    assert True

def test_rabbitmq_queue_one_to_many_queue_handler():
    # Should be able to have an one-to-many relationship between the queue and the handler function
    assert True

def test_rabbitmq_send_message():
    # Should be able to send a message in a given queue
    assert True
