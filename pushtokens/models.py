from django.db import models

# Create your models here.

class Token(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    device_token = models.CharField(max_length=255, default="", db_column="deviceToken")
    stream_token = models.CharField(max_length=255, default="", db_column="currentStreamToken")
    user_id = models.CharField(max_length=255, unique=True, db_column="userID")

    class Meta:
    	db_table = 'device'

class PushConfiguration(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    topic = models.CharField(max_length=255)
    key_file_name = models.CharField(max_length=255, default="")
    use_sandbox = models.BooleanField(default=False)

    class Meta:
        unique_together = ('topic', 'use_sandbox')

    def __str__(self):
        return f"{self.topic} - use_sandbox: {self.use_sandbox}"

class PushMessage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    push_configuration = models.ForeignKey('PushConfiguration', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(default="", null=True, blank=True)
    sound = models.CharField(max_length=255, default="default")
    badge = models.BooleanField(default=True)
    content_available = models.BooleanField(default=True)
    identifier = models.CharField(max_length=255, unique=True)

    last_sent = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title}"