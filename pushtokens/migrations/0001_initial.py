# Generated by Django 3.1.3 on 2020-11-09 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('device_token', models.CharField(max_length=255)),
                ('stream_token', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
