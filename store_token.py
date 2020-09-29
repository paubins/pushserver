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

db = dataset.connect('postgresql://pushserver:rdbUYT8nFrnMyWwbxRvduikM@localhost:5432/pushserver')
#db = dataset.connect('sqlite:///:memory:')
#db = dataset.connect('postgresql://ufbivs448r9cld:pf12a43043cf88b2d44ba0e4242e4c479f4178e83b0c09f24fb25e33e6eba7bc8@ec2-35-169-44-206.compute-1.amazonaws.com:5432/d1b202fii8499b')

@route('/storeDeviceToken', method='POST')
def feedback():
	device = request.json
	table = db['fakefacecall']
	user_id = table.find_one(userID=device["userID"])
	if not user_id:
		table.insert(dict(userID=device["userID"], deviceToken=device["deviceToken"]))

run(host='0.0.0.0', port=8080)
