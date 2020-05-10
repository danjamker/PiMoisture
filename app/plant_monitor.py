# import RPi.GPIO as GPIO
import pika
import os
import time
import json

message_interval = 20  # seconds
reading_interval = 5  # seconds
sensor = 11 # might need to be changed depending on the pi setup
pin = 4 # might need to be changed depending on the pi setup

#Access the CLODUAMQP_URL environment variable
url = os.environ.get('CELERY_BROKER_URL')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
# start a channel
channel = connection.channel()
# Declare a queue
channel.queue_declare(queue='moisture')

isSimulation = 1
if isSimulation:
  import random
  def genrand():
      return random.random(), random.random() * 10
else:
  import Adafruit_DHT

while True:
  body = []
  timeout = time.time() + message_interval
  while True:
    if time.time() > timeout:
      break
    if isSimulation:
      humidity, temperature = genrand()
    else:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    read_time = time.time()
    d = {'t': read_time, 'T': temperature, 'H': humidity, 'h':os.environ.get("NAME")}
    body.append(d)
    time.sleep(reading_interval)

    print('sending data')
    channel.basic_publish(exchange='',
                        routing_key="moisture",
                        body=json.dumps(body))

connection.close()