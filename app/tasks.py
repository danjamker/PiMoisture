import pika, os, json
from datetime import datetime
from couchdb import Server, Document
from couchdb.mapping import TextField, IntegerField, DateTimeField, FloatField

url = os.environ.get('CELERY_BROKER_URL')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

def store(ch, method, properties, body):
    print(ch)
    print(method)
    print(properties)
    body = json.loads(body)
    print(body)
    for v in body:
        insert_value(v)

class Record(Document):
    host = TextField()
    messurement = FloatField()
    time = DateTimeField(default=datetime.now())

def insert_value(body):
    print("[X] Received time:" + str(body["t"]) + " and temperature: " + str(body["T"]))
    try:
        print(os.environ["COUCH_URI"])
        couch = Server("http://admin:couchdb@couchdb:5984/")
        dbname = "plant"
        if dbname in couch:
            db = couch[dbname]
        else:
            db = couch.create(dbname)

        messurment = Record(host=body["h"], messurement=body["T"])
        db.save(messurment)

        print(messurment, "Record inserted successfully into weather table")

    except Exception as error:
        print("Error while connecting to CouchDB", error)



channel.basic_consume('moisture', store, auto_ack=True)
print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()