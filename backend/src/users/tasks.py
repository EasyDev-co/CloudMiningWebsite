import os
import requests
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from config.celery import app
from .utils import send_email


load_dotenv()

User = get_user_model()


BASE_URL = os.environ.get("BASE_URL")


@app.task(bind=True, default_retry_delay=5 * 60)
def send_email_for_user(self, data):
    """
    Добавляет отправку сообщения пользователю
    в очередь Celery

    При ошибке повторная попытка отправить сообщение
    произойдет через 1 минуту
    """
    try:
        send_email(
            data=data
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task(bind=True, default_retry_delay=5 * 60)
def create_user_wallet(self, access_token):
    """
    Добавляет создание кошелька пользователю
    в очередь Celery

    При ошибке повторная попытка отправить сообщение
    произойдет через 1 минуту
    """

    auth_data = {
            'Authorization': f'Bearer {access_token}'
        }
    try:
        requests.post(
            url=BASE_URL + '/api/v1/users/create',
            headers=auth_data
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
