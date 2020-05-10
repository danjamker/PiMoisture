import pika, os, json
from datetime import datetime
import pymongo

url = os.environ.get('CELERY_BROKER_URL')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='weather') # Declare a queue

def store(ch, method, properties, body):
    print(ch)
    print(method)
    print(properties)
    body = json.loads(body)
    print(body)
    for v in body:
        insert_value(v)


def insert_value(body):
    print("[X] Received time:" + str(body["t"]) + " and temperature: " + str(body["T"]))
    try:
        client = pymongo.MongoClient(os.environ["MONGO_URI"])
        db = client["home"]
        col = db["plant"]

        result = col.insert(
            {"messurement": "moisture", "value": body["T"], "host": body["h"], "time": datetime.fromtimestamp(body["t"])})
        print(result, "Record inserted successfully into weather table")

    except (Exception, pymongo.errors) as error:
        print("Error while connecting to MongoDB", error)
    finally:
        # closing database connection.
        if (client):
            client.close()
            print("MongoDB connection is closed")


channel.basic_consume('moisture', store, auto_ack=True)
print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()