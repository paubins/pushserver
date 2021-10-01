# from pushjack_http2 import APNSSandboxClient

# message = {
#     "aps" : {
#     "alert" : {
#         "title" : "Game Request",
#         "subtitle" : "Five Card Draw",
#         "body" : "Bob wants to play poker",
#         },
#         "category" : "GAME_INVITATION"
#     },
#     "gameID" : "12345678"
# }

# client = APNSSandboxClient(certificate='/Users/paubins/projects/pushserver/apns-dev-cert.pem')

# # Send to single device.
# # NOTE: Keyword arguments are optional.
# res = client.send("0d032a27635ee28d5d5937015a723418dd6619e7bc7f6fb7281b0b071b2a7c56", message)

# print(res.errors)
# print(res.token_errors)


# import asyncio
# from uuid import uuid4
# from aioapns import APNs, NotificationRequest, PushType


# async def run():
#     apns_cert_client = APNs(
#         client_cert='/Users/paubins/projects/pushserver/apns-dev-cert.pem',
#         use_sandbox=True,
#     )
#     request = NotificationRequest(
#         device_token='0d032a27635ee28d5d5937015a723418dd6619e7bc7f6fb7281b0b071b2a7c56',
#         message = {
#             "aps": {
#                 "alert": "Hello from APNs",
#                 "badge": "1",
#             }
#         },
#         notification_id=str(uuid4()),  # optional
#         time_to_live=3,                # optional
#         push_type=PushType.ALERT,      # optional
#     )
#     await apns_cert_client.send_notification(request)
#     return False

# # loop = asyncio.get_event_loop()
# asyncio.run(run())


# from pyapns_client import APNSClient, IOSPayloadAlert, IOSPayload, IOSNotification, APNSException, UnregisteredException


# cli = APNSClient(mode=APNSClient.MODE_DEV, client_cert='/Users/paubins/projects/pushserver/apns-dev-cert.pem')
# alert = IOSPayloadAlert(body='body!', title='title!')
# payload = IOSPayload(alert=alert)
# notification = IOSNotification(payload=payload, priority=IOSNotification.PRIORITY_LOW)

# try:
#     cli.push(notification=notification, device_token='0d032a27635ee28d5d5937015a723418dd6619e7bc7f6fb7281b0b071b2a7c56')
# except APNSException as e:
#     if e.is_device_error:
#         if isinstance(e, UnregisteredException):
#             # device is unregistered, compare timestamp (e.timestamp_datetime) and remove from db
#             pass
#         else:
#             # flag the device as potentially invalid
#             pass
#     elif e.is_apns_error:
#         # try again later
#         pass
#     elif e.is_programming_error:
#         # check your code
#         # try again later
#         pass
# else:
#     # everything is ok
#     pass


# from apns import APNs, Payload

# apns = APNs(cert_file='certificate.pem', key_file='apns-dev-cert.pem')

# token = '0d032a27635ee28d5d5937015a723418dd6619e7bc7f6fb7281b0b071b2a7c56'
# payload = Payload(alert="Hello World!", sound="default", badge=1)
# apns.gateway_server.send_notification(token, payload)


from apns2.client import APNsClient
from apns2.payload import Payload
import collections

token_hex = '0d032a27635ee28d5d5937015a723418dd6619e7bc7f6fb7281b0b071b2a7c56'
payload = Payload(alert="Hello World!", sound="default", badge=1)
topic = 'com.paubins.LiveVideoShare'
client = APNsClient('apns-dev-cert.pem', use_sandbox=True, use_alternative_port=False)
client.send_notification(token_hex, payload, topic)

# # To send multiple notifications in a batch
# Notification = collections.namedtuple('Notification', ['token', 'payload'])
# notifications = [Notification(payload=payload, token=token_hex)]
# client.send_notification_batch(notifications=notifications, topic=topic)



# # To use token based authentication
# from apsn2.credentials import TokenCredentials

# auth_key_path = 'path/to/auth_key'
# auth_key_id = 'app_auth_key_id'
# team_id = 'app_team_id'
# token_credentials = TokensCredentials(auth_key_path=auth_key_path, auth_key_id=auth_key_id, team_id=team_id)
# client = APNsClient(credentials=token_credentials, use_sanbox=False)
# client.send_notification_batch(notifications=notifications, topic=topic)

