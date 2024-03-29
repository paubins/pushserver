# Generated by Django 3.1.3 on 2020-11-09 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pushtokens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('topic', models.CharField(max_length=255, unique=True)),
                ('key_file_name', models.CharField(default='', max_length=255)),
                ('use_sandbox', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='token',
            name='device_token',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='token',
            name='stream_token',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.CreateModel(
            name='PushMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('sound', models.CharField(default='default', max_length=255)),
                ('badge', models.BooleanField(default=True)),
                ('content_available', models.BooleanField(default=True)),
                ('identifer', models.CharField(max_length=255, unique=True)),
                ('custom_json_render', models.TextField(null=True)),
                ('push_configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pushtokens.pushconfiguration')),
            ],
        ),
    ]
