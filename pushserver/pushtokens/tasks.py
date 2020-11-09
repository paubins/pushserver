from apns2.client import APNsClient
from apns2.payload import Payload, PayloadAlert
from urllib.parse import urlsplit, parse_qs

import collections

from celery import shared_task

@shared_task
def debug_task(self):
    print(f'Request: {self.request!r}')

@shared_task
def push_message(push_message_obj, device_token, custom=None):
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

    payload.body = push_message_obj.body
    topic = push_message_obj.topic
    client = APNsClient(push_message_obj.push_configuration.key_file_name, 
        use_sandbox=push_message_obj.push_configuration.use_sandbox,
        use_alternative_port=False)
    client.send_notification(device_token, payload, topic)


@shared_task
def push_message_batch(push_message, device_tokens, custom=None):
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

    payload.body = push_message_obj.body
    topic = push_message_obj.topic

    client = APNsClient(push_message_obj.push_configuration.key_file_name, 
        use_sandbox=push_message_obj.push_configuration.use_sandbox,
        use_alternative_port=False)
    
    # To send multiple notifications in a batch
    Notification = collections.namedtuple('Notification', ['token', 'payload'])
    notifications = []
    for device_token in device_tokens:
        notifications += [Notification(payload=payload, token=device_token.device_token)]

    client.send_notification_batch(notifications=notifications, topic=topic)
 