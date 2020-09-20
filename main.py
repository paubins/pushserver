from bottle import route, run, template
from bottle import request, route, run
import sqlite3
import dataset
import os
import sys

from apns2.client import APNsClient
from apns2.payload import Payload
from urllib.parse import urlsplit, parse_qs

import collections

async def sendToken(device_token):
    apns_cert_client = APNs(
        client_cert='./apns-dev-cert.pem',
        use_sandbox=True,
    )
    request = NotificationRequest(
        device_token=device_token,
        message = {
            "aps": {
                "alert": "Hello from APNs",
                "badge": "1",
            }
        },
        notification_id=str(uuid4()),  # optional
        time_to_live=3,                # optional
        push_type=PushType.ALERT,      # optional
    )
    await apns_cert_client.send_notification(request)


#db = dataset.connect('postgresql://pushserver:rdbUYT8nFrnMyWwbxRvduikM@localhost:5432/pushserver')
db = dataset.connect('sqlite:///:memory:')

@route('/publish/', method='POST')
def index():
    query = parse_qs(request.body.getvalue().decode('utf-8'))
    table = db['device']
    streamToken = query["name"][0]
    user = table.find_one(currentStreamToken=streamToken)
    print(user)
    if not user:
        return

    table.update(dict(currentStreamToken=streamToken), ["streamToken"])
    token_hex = user["deviceToken"]
    payload = Payload(alert=streamToken, sound="default", badge=1, content_available=1)
    topic = 'com.paubins.LiveVideoShare'
    client = APNsClient('apns-dev-cert.pem', use_sandbox=True, use_alternative_port=False)
    client.send_notification(token_hex, payload, topic)

@route('/checkStream', method='POST')
def checkStream():
    device = request.json
    print(device)
    
    table = db['device']
    user_id = table.find_one(userID=device["userID"])
    if user_id and user_id["currentStreamToken"]:
        print("streaming is")
        return {"streaming" : "true"}
    else:
        return {"streaming" : "false"}
 
@route('/resetToken/', method='POST')
def reset():
    query = parse_qs(request.body.getvalue().decode('utf-8'))
    table = db['device']
    user_id = table.find_one(currentStreamToken=query["name"])
    if user_id:
        table.update(dict(userID=user_id["userID"], currentStreamToken=""), ['userID'])

        token_hex = user_id["deviceToken"]
        payload = Payload(alert="Stream has ended", sound="default", badge=1, content_available=1)
        topic = 'com.paubins.LiveVideoShare'
        client = APNsClient('apns-dev-cert.pem', use_sandbox=True, use_alternative_port=False)
        client.send_notification(token_hex, payload, topic)
 
@route('/storeStreamToken', method='POST')
def storeStreamToken():
    device = request.json
    table = db['device']
    user_id = table.find_one(userID=device["userID"])
    if user_id:
        table.update(dict(userID=device["userID"], currentStreamToken=device["streamToken"]), ['userID'])

@route('/feedback', method='POST')
def feedback():
	device = request.json
	table = db['device']
	user_id = table.find_one(userID=device["userID"])
	if not user_id:
		table.insert(dict(userID=device["userID"], currentStreamToken="", deviceToken=device["deviceToken"]))



run(host='0.0.0.0', port=8080)
