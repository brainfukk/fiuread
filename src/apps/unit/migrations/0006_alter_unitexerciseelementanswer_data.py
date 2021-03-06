# Generated by Django 3.2.7 on 2021-09-29 08:58

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unit", "0005_alter_unitexerciseelementanswer_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unitexerciseelementanswer",
            name="data",
            field=models.JSONField(
                default={"answers": {0: 1}, "variants": ["data"]},
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                verbose_name="Варинаты ответов или правильные ответы(зависит от типа упражнения)",
            ),
        ),
    ]
