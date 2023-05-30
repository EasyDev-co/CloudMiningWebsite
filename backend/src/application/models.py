from django.db import models


class Difficulty(models.Model):
    class Meta:
        verbose_name = 'сложность'
        verbose_name = 'Данные о сложности'

    difficulty = models.BigIntegerField(
        verbose_name='Сложность',
        default=49549703178593
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )


class Reward(models.Model):
    class Meta:
        verbose_name = 'награда'
        verbose_name = 'Данные о награде'

    reward_block = models.FloatField(
        verbose_name='Награда',
        default=6.81
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )


class Contract(models.Model):
    class Meta:
        verbose_name = 'контракт'
        verbose_name = 'Контракты'

    # customer = models.ForeignKey(
    #     Users,
    #     verbose_name='Заказчик',
    #     on_delete=models.CASCADE,
    #     related_name='is_customer'
    # )
    hashrate = models.FloatField(verbose_name='Хешрейт')
    contract_start = models.DateTimeField(verbose_name='Начало')
    contract_end = models.DateTimeField(verbose_name='Завершение')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
