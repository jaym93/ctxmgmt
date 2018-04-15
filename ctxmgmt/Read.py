#! /usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import SimpleMFRC522
from gyro import get_magnitude
from location import get_location
import re
import datetime
import time
import psutil
import urllib2
import requests
import json

device_name = "device one"

reader = SimpleMFRC522.SimpleMFRC522()
while True:
    packet = {}
    # print(get_magnitude())
    if(get_magnitude() > 1):  
        new_id,text = reader.read()
        packet['what'] = device_name
        packet['who_id'] = new_id
        packet['who'] = text.strip()
        location = get_location('rpi')
        if location['message'] == 'ok':
            packet['where'] = location['loc']
        else:
            packet['where'] = "unknown location"
        packet['sno'] = str(time.time())
        packet['when'] = time.strftime('%m/%d/%Y %I:%M:%S %p')
        packet['meta'] = {'cpu': str(psutil.cpu_percent())+'%', 'memory':str(psutil.virtual_memory().percent)+'%', 'disk':str(psutil.disk_usage('/').percent)+'%'}
        print(str(packet))
        aws_url = 'https://ao9kkk5kze.execute-api.us-east-1.amazonaws.com/testing/'
        head = {'Content-Type':'application/json'}
        r = requests.post(aws_url, json.dumps(packet), headers=head)
        print('RESP '+str(r.json()))
    
GPIO.cleanup()
