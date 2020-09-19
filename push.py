#!/usr/bin/env python
import ssl
import json
import socket
import struct
import binascii


def send_push_message(token, payload):
    # the certificate file generated from Provisioning Portal
    certfile = 'certificate.pem'
 
    # APNS server address (use 'gateway.push.apple.com' for production server)
    apns_address = ('gateway.sandbox.push.apple.com', 2195)
 
    # create socket and connect to APNS server using SSL
    s = socket.socket()
    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=certfile)
    sock.connect(apns_address)
 
    # generate APNS notification packet
    token = binascii.unhexlify(token)
    fmt = "!cH32sH{0:d}s".format(len(payload))
    cmd = '\x00'
    msg = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
    sock.write(msg)
    sock.close()
 

payload = {"aps": {"alert" : "You got your emails.", "badge": 9, "sound": "bingbong.aiff"}}
send_push_message("0d032a27635ee28d5d5937015a723418dd6619e7bc7f6fb7281b0b071b2a7c56", json.dumps(payload))