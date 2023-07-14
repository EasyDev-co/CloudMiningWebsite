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
    'Get_block_data_task': {
        'task': 'src.application.tasks.save_new_block_data_in_db',
        'schedule': crontab(),  # crontab() runs the tasks every minute
    },
    'Get_btc_price_task': {
        'task': 'src.application.tasks.save_new_btc_price_in_db',
        'schedule': crontab(),  # crontab() runs the tasks every minute
    },
    'Get_eth_price_task': {
        'task': 'src.application.tasks.save_new_eth_price_in_db',
        'schedule': crontab(),  # crontab() runs the tasks every minute
    }
}
