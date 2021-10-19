# Generated by Django 3.2.7 on 2021-10-14 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0010_unittheoryelement_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitexerciseelement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='unitassets'),
        ),
        migrations.AddField(
            model_name='unitexerciseelement',
            name='order_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='unitexerciseelement',
            name='content',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Контент элемента'),
        ),
        migrations.AlterField(
            model_name='unittheoryelement',
            name='type',
            field=models.CharField(choices=[('LIST_VIEW', 'Список'), ('PLAIN_TEXT_VIEW', 'Текст'), ('IMAGE_VIEW', 'Изображение'), ('HEADING', 'Заголовок')], max_length=60, verbose_name='Тип элемента'),
        ),
    ]