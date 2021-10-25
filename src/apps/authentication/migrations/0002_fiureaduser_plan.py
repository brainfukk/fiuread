# Generated by Django 3.2.7 on 2021-10-25 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiureaduser',
            name='plan',
            field=models.CharField(choices=[('FREE_PLAN', 'Бесплатная подписка'), ('PREMIUM_PLAN', 'Премиальная подписка')], default='FREE_PLAN', max_length=30, verbose_name='Подписка пользователя'),
        ),
    ]
