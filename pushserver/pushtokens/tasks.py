from apns2.client import APNsClient
from apns2.payload import Payload, PayloadAlert
from urllib.parse import urlsplit, parse_qs

from .models import PushMessage, Token

import collections

from celery import shared_task

@shared_task
def debug_task(self):
    print(f'Request: {self.request!r}')


def get_push_client(push_message_obj_id, custom=None):
    push_message_obj = PushMessage.objects.get(pk=push_message_obj_id)
    payload = None
    if custom:
        payload = Payload(alert=push_message_obj.title,
            sound=push_message_obj.sound,
            badge=push_message_obj.badge,
            custom=custom,
            content_available=push_message_obj.badge)
    else:
        payload = Payload(alert=push_message_obj.title,
            sound=push_message_obj.sound,
            badge=push_message_obj.badge,
            content_available=push_message_obj.badge)

    if push_message_obj.body:
        payload.body = push_message_obj.body
    topic = push_message_obj.push_configuration.topic
    client = APNsClient(push_message_obj.push_configuration.key_file_name, 
        use_sandbox=push_message_obj.push_configuration.use_sandbox,
        use_alternative_port=False)

    return (client, payload, topic)

@shared_task
def push_message(push_message_obj_id, device_token, custom=None):
    client, payload, topic = get_push_client(push_message_obj_id, custom=None)
    client.send_notification(device_token, payload, topic)


@shared_task
def push_message_batch(push_message_obj_id, device_token_ids, custom=None):
    client, payload, topic = get_push_client(push_message_obj_id, custom=None)
    
    # To send multiple notifications in a batch
    Notification = collections.namedtuple('Notification', ['token', 'payload'])
    notifications = []
    device_tokens = Token.objects.in_bulk(device_token_ids)
    for key, device_token in device_tokens.items():
        notifications += [Notification(payload=payload, token=device_token.device_token)]

    client.send_notification_batch(notifications=notifications, topic=topic)
 