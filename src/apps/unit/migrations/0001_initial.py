# Generated by Django 3.2.7 on 2021-09-22 15:53

import django.core.serializers.json
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время создания объекта"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Время последнего обновления объекта",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название топика"),
                ),
            ],
            options={
                "verbose_name": "Топик",
                "verbose_name_plural": "Топики",
            },
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время создания объекта"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Время последнего обновления объекта",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="Безымянный раздел",
                        max_length=255,
                        verbose_name="Название юнита",
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="units",
                        to="unit.topic",
                        verbose_name="Топик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Юнит",
                "verbose_name_plural": "Юниты",
            },
        ),
        migrations.CreateModel(
            name="UnitTheoryElement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время создания объекта"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Время последнего обновления объекта",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("LIST_VIEW", "List View"),
                            ("PLAIN_TEXT_VIEW", "Plain Text View"),
                            ("IMAGE_VIEW", "Image View"),
                            ("IMAGE_LEFT_TEXT_VIEW", "Image Left Text View"),
                            ("IMAGE_RIGHT_TEXT_VIEW", "Image Right Text View"),
                        ],
                        max_length=60,
                        verbose_name="Тип элемента",
                    ),
                ),
                (
                    "content",
                    models.JSONField(
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        verbose_name="Контетнт элемента",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="theories",
                        to="unit.unit",
                        verbose_name="Юнит",
                    ),
                ),
            ],
            options={
                "verbose_name": "Теоретический блок юнита",
                "verbose_name_plural": "Теоретическии блоки юнитов",
            },
        ),
        migrations.CreateModel(
            name="UnitExerciseElement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время создания объекта"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Время последнего обновления объекта",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("SELECT_VIEW", "Select View"),
                            ("TRUE_OR_FALSE_VIEW", "True Or False View"),
                            ("FREE_ANSWER_VIEW", "Free Answer View"),
                        ],
                        max_length=60,
                        verbose_name="Тип элемента",
                    ),
                ),
                (
                    "content",
                    models.JSONField(
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        verbose_name="Контент элемента",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises",
                        to="unit.unit",
                        verbose_name="Юнит",
                    ),
                ),
            ],
            options={
                "verbose_name": "Упражнение юнита",
                "verbose_name_plural": "Упражнения юнитов",
            },
        ),
    ]
