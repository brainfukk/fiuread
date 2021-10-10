# Generated by Django 3.2.7 on 2021-09-29 08:56

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0004_auto_20210929_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitexerciseelementanswer',
            name='data',
            field=models.JSONField(default={'answers': {0: 1}, 'variants': ['d', 'a', 't', 'a']}, encoder=django.core.serializers.json.DjangoJSONEncoder, verbose_name='Варинаты ответов или правильные ответы(зависит от типа упражнения)'),
        ),
    ]
