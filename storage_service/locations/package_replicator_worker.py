#!/usr/bin/env python
import pika
import random
import time


# RabbitMQ Configuration
# TODO: get some of this from settings config.
RMQ_HOST = 'localhost'
PACKAGE_REPLICATION_QUEUE = 'package_replication_queue'
RMQ_CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=RMQ_HOST))
RMQ_CHANNEL = RMQ_CONNECTION.channel()
RMQ_CHANNEL.queue_declare(
    queue=PACKAGE_REPLICATION_QUEUE, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(random.random() * 5)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


RMQ_CHANNEL.basic_qos(prefetch_count=1)
RMQ_CHANNEL.basic_consume(callback, queue=PACKAGE_REPLICATION_QUEUE)
RMQ_CHANNEL.start_consuming()
