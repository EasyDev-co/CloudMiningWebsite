from django.contrib.auth import get_user_model
from config.celery import app
from .utils import send_email


User = get_user_model()


@app.task(bind=True, default_retry_delay=5 * 60)
def send_email_for_user(self, data):
    print('Попал в send_email task')
    try:
        send_email(
            data=data
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)