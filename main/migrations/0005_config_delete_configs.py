# Generated by Django 4.0.6 on 2022-10-06 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_configs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_name', models.CharField(blank=True, max_length=60, verbose_name='Конфигурация')),
                ('config_value', models.IntegerField(blank=True, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
            },
        ),
        migrations.DeleteModel(
            name='Configs',
        ),
    ]
