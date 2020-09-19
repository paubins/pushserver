from bottle import route, run, template
from bottle import request, route, run
import sqlite3
import dataset

from apns2.client import APNsClient
from apns2.payload import Payload
import collections

async def sendToken(device_token):
    apns_cert_client = APNs(
        client_cert='/Users/paubins/projects/pushserver/apns-dev-cert.pem',
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


db = dataset.connect('sqlite:///:memory:')

@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return str(result)

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/publish', method='POST')
def index():
    device = request.json
    table = db['device']
    user = table.find_one(streamToken=device["streamToken"])
    if not user:
        device_token = user["deviceToken"]

    return {
    	"aps" : {
    	"alert" : {
	    	"title" : "Game Request",
	    	"subtitle" : "Five Card Draw",
	    	"body" : "Bob wants to play poker",
    		},
    		"category" : "GAME_INVITATION"
    	},
    	"gameID" : "12345678"
    }

@route('/storeStreamToken', method='POST')
def storeStreamToken():
    device = request.json
    print(device)
    
    table = db['device']
    user_id = table.find_one(userID=device["userID"])
    if not user_id:
        print("not found")
        table.update(dict(userID=device["userID"], currentStreamToken=device["streamToken"]), ['userID'])

    token_hex = user_id["deviceToken"]
    payload = Payload(alert=device["streamToken"], sound="default", badge=1)
    topic = 'com.paubins.LiveVideoShare'
    client = APNsClient('apns-dev-cert.pem', use_sandbox=True, use_alternative_port=False)
    client.send_notification(token_hex, payload, topic)


@route('/feedback', method='POST')
def feedback():
	device = request.json
	
	table = db['device']
	user_id = table.find_one(userID=device["userID"])
	if not user_id:
		print("not found")
		table.insert(dict(userID=device["userID"], currentStreamToken="", deviceToken=device["deviceToken"]))
	print(device["userID"])
	print(device)



run(host='0.0.0.0', port=8080)
