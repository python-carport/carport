# Generated by Django 2.2.2 on 2019-07-24 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carport', '0002_auto_20190724_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='begin_hours',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='record',
            name='end_hours',
            field=models.DateTimeField(),
        ),
    ]
