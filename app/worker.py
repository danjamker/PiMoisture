import os
from celery import Celery

app = Celery(
  broker=os.environ['CELERY_BROKER_URL'],
  include=('tasks',))

app.conf.beat_schedule = {
  'refresh': {
    'task': 'log_mosture',
    'schedule': float(1),
    'args': ("demo",90, )
  },
}