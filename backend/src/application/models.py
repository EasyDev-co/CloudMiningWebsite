from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Difficulty(models.Model):
    class Meta:
        verbose_name = 'сложность'
        verbose_name_plural = 'Данные о сложности'

    id = models.CharField(primary_key=True, max_length=20, default='difficulty')
    difficulty = models.BigIntegerField(
        verbose_name='Сложность',
        default=49549703178593
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )


class Reward(models.Model):

    id = models.CharField(primary_key=True, max_length=20, default='reward_block')
    reward_block = models.FloatField(
        verbose_name='Награда',
        default=6.81
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'награда'
        verbose_name_plural = 'Данные о награде'


class MaintenanceCost(models.Model):

    id = models.CharField(primary_key=True, max_length=20, default='maintenance_cost')
    coast = models.FloatField(
        verbose_name='Стоимость',
        default=0
    )

    class Meta:
        verbose_name = 'стоимость обслуживания'
        verbose_name_plural = 'Данные о стоимости обслуживания'


class BtcPrice(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default='btc_price')
    price = models.FloatField(
        verbose_name='Стоимость',
        default=0
    )

    class Meta:
        verbose_name = 'стоимость btc (в usd)'
        verbose_name_plural = 'Данные о стоимости биткоина (в usd)'


class Contract(models.Model):

    customer = models.ForeignKey(
        User,
        to_field='uuid',
        verbose_name='Заказчик',
        on_delete=models.CASCADE,
        related_name='is_customer'
    )
    hashrate = models.FloatField(verbose_name='Хешрейт')
    contract_start = models.DateField(verbose_name='Начало')
    contract_end = models.DateField(verbose_name='Завершение')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'контракт'
        verbose_name_plural = 'Контракты'
        ordering = ('-created_at',)
