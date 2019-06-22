# Generated by Django 2.2.2 on 2019-06-20 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(db_column='Fld', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('remain', models.FloatField(default=0.0)),
                ('credit', models.FloatField(default=5.0)),
            ],
        ),
        migrations.CreateModel(
            name='Carport',
            fields=[
                ('id', models.IntegerField(db_column='Fld', primary_key=True, serialize=False)),
                ('using', models.CharField(max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carport.User')),
            ],
        ),
    ]