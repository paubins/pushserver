from django.contrib import admin

# Register your models here.
from .models import Token, PushConfiguration, PushMessage
from .tasks import push_message, push_message_batch

from django.contrib import messages

import datetime

def make_send_push_notification(message):
    def send_push_notification(modeladmin, request, queryset):
        device_tokens = list(queryset.values_list('id', flat=True))
        print(device_tokens)
        push_message_batch.delay(message.pk, device_tokens)
        message.last_sent = datetime.datetime.now()
        message.save()
        messages.info(request, "Message: \"{0}\" has been pushed to {1} devices".format(message,
                                                                  len(queryset)))

    send_push_notification.short_description = "Push notification: {0}".format(message)
    # We need a different '__name__' for each action - Django
    # uses this as a key in the drop-down box.
    send_push_notification.__name__ = 'push_notification_{0}'.format(message.id)

    return send_push_notification

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'date_updated', 'user_id', 'device_token', 'stream_token']
    search_fields = ['user_id', 'device_token']

    def get_actions(self, request):
        actions = super().get_actions(request)
        for message in PushMessage.objects.all():
            action = make_send_push_notification(message)
            actions[action.__name__] = (action,
                                    action.__name__,
                                    action.short_description)
        return actions

@admin.register(PushConfiguration)
class PushConfigurationAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'date_updated', 'topic', 'key_file_name', 'use_sandbox']

@admin.register(PushMessage)
class PushMessageAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'date_updated', 'last_sent', 'push_configuration', 'title', 'sound', 'badge', 'content_available']
