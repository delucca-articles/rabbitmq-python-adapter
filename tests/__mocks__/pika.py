class Channel:
    def __init__(self): pass
    def exchange_declare(self): pass
    def queue_declare(self): pass
    def queue_bind(self): pass
    def basic_qos(self): pass
    def basic_consume(self): pass
    def start_consuming(self): pass
    def basic_publish(self): pass
    def basic_ack(self): pass

class Connection:
    def __init__(self): pass
    def channel(self): return Channel()
