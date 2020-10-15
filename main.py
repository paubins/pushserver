from bottle import route, run, template
from bottle import request, route, run
import sqlite3
import dataset
import os
import sys

from apns2.client import APNsClient
from apns2.payload import Payload, PayloadAlert
from urllib.parse import urlsplit, parse_qs

import collections

db = dataset.connect('postgresql://pushserver:rdbUYT8nFrnMyWwbxRvduikM@localhost:5432/pushserver')
#db = dataset.connect('sqlite:///:memory:')
#db = dataset.connect('postgresql://ufbivs448r9cld:pf12a43043cf88b2d44ba0e4242e4c479f4178e83b0c09f24fb25e33e6eba7bc8@ec2-35-169-44-206.compute-1.amazonaws.com:5432/d1b202fii8499b')

@route('/vid/<streamToken>', method='GET')
def get_vid(streamToken):
    return template("templates/token.html", {"token" : streamToken})

@route('/publish/', method='POST')
def index():
    query = parse_qs(request.body.getvalue().decode('utf-8'))
    print(query)
    table = db['device']
    streamToken = query["name"][0]
    user = table.find_one(currentStreamToken=streamToken)
    print(user)
    if not user:
        return

    table.update(dict(currentStreamToken=streamToken), ["streamToken"])
    token_hex = user["deviceToken"]
    payload = Payload(alert=PayloadAlert(title="Live stream has started", body="View your stream from Wideshot"), custom={"streamToken" : streamToken}, sound="default", badge=1, content_available=1)
    topic = 'com.paubins.LiveVideoShare'
    client = APNsClient('apns-dev-cert-prod.pem', use_sandbox=False, use_alternative_port=False)
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
        payload = Payload(alert="Wideshot stream has ended", sound="default", badge=1, content_available=1)
        topic = 'com.paubins.LiveVideoShare'
        client = APNsClient('apns-dev-cert-prod.pem', use_sandbox=False, use_alternative_port=False)
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
    else:
        table.update(dict(userID=device["userID"], deviceToken=device["deviceToken"]), ['userID'])


run(host='0.0.0.0', port=8080)
