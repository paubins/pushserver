# Generated by Django 3.1.3 on 2020-11-10 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushtokens', '0008_auto_20201110_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='device_token',
            field=models.CharField(db_column='deviceToken', default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='token',
            name='stream_token',
            field=models.CharField(db_column='currentStreamToken', default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='token',
            name='user_id',
            field=models.CharField(db_column='userID', max_length=255, unique=True),
        )
    ]
