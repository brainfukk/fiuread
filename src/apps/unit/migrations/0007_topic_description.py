# Generated by Django 3.2.7 on 2021-10-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unit", "0006_alter_unitexerciseelementanswer_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="description",
            field=models.CharField(
                blank=True, default="", max_length=40, verbose_name="Описание раздела"
            ),
        ),
    ]
