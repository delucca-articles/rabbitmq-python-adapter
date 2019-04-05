import sys
import os

sys.path.append(os.environ['CONFIG'])
from config import *

def subscribe(
    channel,
    handler,
    queue=config.rabbitmq.queue,
    durable=config.rabbitmq.durable,
    exchange=config.rabbitmq.exchange,
    prefetch_count=config.rabbitmq.prefetch.count
):
    channel.queue_declare(queue=queue, durable=durable)
    channel.queue_bind(queue=queue, exchange=exchange)
    channel.basic_qos(prefetch_count=prefetch_count)
    channel.basic_consume(queue=queue, on_message_callback=handler)
