# redis for Celery
import os
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()


CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_BEAT_SCHEDULE = {  # scheduler configuration
    'Task_one_schedule': {  # whatever the name you want
        'task': 'src.application.tasks.get_orders_for_save_in_db',  # name of task with path
        'schedule': crontab(),  # crontab() runs the tasks every minute
    }
}
