# Generated by Django 3.1.3 on 2020-11-09 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushtokens', '0004_remove_pushmessage_custom_json_render'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushmessage',
            name='body',
            field=models.CharField(default='', max_length=255),
        ),
    ]
