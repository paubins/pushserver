# Generated by Django 3.1.3 on 2020-11-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushtokens', '0009_auto_20201110_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushmessage',
            name='body',
            field=models.TextField(default='', null=True),
        ),
    ]
