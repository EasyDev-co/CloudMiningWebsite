from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Номер телефона',
        error_messages={
            "max_length": _("A telephone number cannot have more than 15 digits")
        }
                                    )
    text = models.TextField(verbose_name='Текст')
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    is_published = models.BooleanField(
        default=False, verbose_name='Опубликован'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)
