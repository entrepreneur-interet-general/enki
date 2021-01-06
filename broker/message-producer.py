from json import dumps
from kafka import KafkaProducer
import time
import os

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:29092")

consumer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: dumps(v).encode('utf-8'))


while True:
    time.sleep(5)
    consumer.send("messages", "test")
    print("Message sent")
