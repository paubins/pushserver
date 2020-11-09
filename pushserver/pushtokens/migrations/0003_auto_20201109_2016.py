# Generated by Django 3.1.3 on 2020-11-09 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushtokens', '0002_auto_20201109_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushconfiguration',
            name='topic',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='pushconfiguration',
            unique_together={('topic', 'use_sandbox')},
        ),
    ]