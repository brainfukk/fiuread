# Generated by Django 3.2.7 on 2021-10-13 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unit", "0008_auto_20211013_1226"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unittheoryelement",
            name="content",
            field=models.CharField(
                blank=True, max_length=600, null=True, verbose_name="Контетнт элемента"
            ),
        ),
    ]
