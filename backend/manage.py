#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from config.settings import (
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD
)


def check_smtp_settings():
    """Проверяет переданные ли данные для отправки сообщений польщователю"""
    smtp_lst = [EMAIL_HOST_PASSWORD, EMAIL_HOST_USER]
    if not all(smtp_lst):
        raise Exception('Не указаны переменные окружения: EMAIL_HOST_PASSWORD, EMAIL_HOST_USER')
    else:
        return True


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if check_smtp_settings():
        main()
