# Generated by Django 3.1.3 on 2020-11-10 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushtokens', '0007_pushmessage_last_sent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pushmessage',
            old_name='identifer',
            new_name='identifier',
        ),
    ]
