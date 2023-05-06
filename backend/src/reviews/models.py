from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)

    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.SET_DEFAULT,
        default='Пользователь удален',
        related_name='created_by'
    )
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    is_published = models.BooleanField(
        default=False, verbose_name='Опубликован'
    )
