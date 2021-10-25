# Generated by Django 3.2.7 on 2021-10-17 04:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("unit", "0012_auto_20211015_0445"),
    ]

    operations = [
        migrations.AddField(
            model_name="unituseranswer",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_answers",
                to="authentication.fiureaduser",
                verbose_name="Пользователь",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="unitexerciseelement",
            name="type",
            field=models.CharField(
                choices=[
                    ("ANSWER_CHOICE", "Выбрать правильный ответ"),
                    ("IN_TEXT_SELECT", "Выбор правильного ответа в тексте"),
                    ("FREE_IN_TEXT_ANSWER", "Вписать правильный ответ в тексте"),
                ],
                max_length=60,
                verbose_name="Тип элемента",
            ),
        ),
        migrations.AlterField(
            model_name="unituseranswer",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="unit.unit",
                verbose_name="Юнит",
            ),
        ),
    ]
