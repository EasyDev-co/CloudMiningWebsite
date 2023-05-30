# Generated by Django 4.2 on 2023-05-30 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_first_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashrate', models.FloatField(verbose_name='Хешрейт')),
                ('contract_start', models.DateTimeField(verbose_name='Начало')),
                ('contract_end', models.DateTimeField(verbose_name='Завершение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Контракты',
            },
        ),
        migrations.AlterModelOptions(
            name='difficulty',
            options={'verbose_name': 'Данные о сложности'},
        ),
        migrations.AlterModelOptions(
            name='reward',
            options={'verbose_name': 'Данные о награде'},
        ),
        migrations.AddField(
            model_name='difficulty',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='reward',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='difficulty',
            name='difficulty',
            field=models.BigIntegerField(default=49549703178593, verbose_name='Сложность'),
        ),
        migrations.AlterField(
            model_name='reward',
            name='reward_block',
            field=models.FloatField(default=6.81, verbose_name='Награда'),
        ),
    ]
