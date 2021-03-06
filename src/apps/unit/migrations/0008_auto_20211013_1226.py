# Generated by Django 3.2.7 on 2021-10-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unit", "0007_topic_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="unittheoryelement",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="unitassets"),
        ),
        migrations.AlterField(
            model_name="unittheoryelement",
            name="type",
            field=models.CharField(
                choices=[
                    ("LIST_VIEW", "Список"),
                    ("PLAIN_TEXT_VIEW", "Текст"),
                    ("IMAGE_VIEW", "Изображение"),
                    ("IMAGE_BETWEEN_TEXT", "Изображение, между текстами"),
                    ("IMAGE_LEFT_TEXT_VIEW", "Изображение, текст слева"),
                    ("IMAGE_RIGHT_TEXT_VIEW", "Изображение, текст справа"),
                    ("HEADING", "Заголовок"),
                ],
                max_length=60,
                verbose_name="Тип элемента",
            ),
        ),
    ]
