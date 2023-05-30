from djoser.email import PasswordResetEmail
from django.contrib.auth.models import User
from config.celery import app


@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_email(self, context, email):
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        PasswordResetEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
