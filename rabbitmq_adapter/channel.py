import pika

def create(host):
    params = pika.URLParameters(host)
    connection = pika.BlockingConnection(params)

    return connection.channel()
