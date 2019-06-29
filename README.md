# RabbitMQ Python Adapter

This repository was created to provide the code samples on the [Recommendation Algorithm Using Python and RabbitMQ (Part 2): Connecting with RabbitMQ](https://medium.com/@odelucca/recommendation-algorithm-using-python-and-rabbitmq-part-2-connecting-with-rabbitmq-aa0ec933e195) article. This module's goal is to make it easier to connect, send and receive messages to a RabbitMQ server. The idea is to handle all complex use cases of a simple RabbitMQ connection and return just a simple object which you can use to interact with your AMQP server.

## 🧐 What's inside

This module has three main methods:

**Channel**: in this method, you can connect with a new RabbitMQ server. This is the basic method. You need a channel in order to use any other method.

**Listener**: with a created channel you can start listening to new messages in a specific queue.

**Sender**: with this method, you can send messages to a specific queue.

## 🤖 Installation Instructions

Copy the contents from the `rabbitmq_adapter` folder to your project folder. Afterward, set the `CONFIG` environment variable to a configuration path where you store all your project's settings. Inside that path create a configuration named `rabbitmq`.

**IMPORTANT**: This module use Dotmap. Don't forget to use it in your settings too.

## 🤟 Usage

First, create a new RabbitMQ channel with the following code:

```
import rabbitmq_adapter

rabbitmq_channel = rabbitmq_adapter.channel.create(<your-rabbitmq-connection-string)
```

With the channel created, you can now start listening to a new queue:

```
rabbitmq_adapter.listener.subscribe(rabbitmq_channel, <your-handler-function>)
```

If you want to publish a new message, you can simply:

```
rabbitmq_adapter.sender.publish(rabbitmq_channel, <your-message>)
```

## ⚙️ Testing

We use Pytest as our testing framework. Every test (unit and integration) are placed inside the `tests` folder. Also, they should follow the following pattern:

```
test_<SCRIPT NAME>.js
```

To test the module, just run:
```
pytest
```

## 💅 Versioning

We use [SemVer](https://semver.org/) as our versioning pattern.

## 📚 Licensing

This module uses the MIT License. You can check it out by [clicking here](LICENSE)
