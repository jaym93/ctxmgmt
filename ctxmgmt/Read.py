#! /usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import SimpleMFRC522
from gyro import get_magnitude
from location import get_location
import re
import time

device_name = "rpi2"

reader = SimpleMFRC522.SimpleMFRC522()
while True:
    packet = {}
    # print(get_magnitude())
    if(get_magnitude() > 1):  
        new_id,text = reader.read()
        packet['what'] = device_name
        packet['who_id'] = new_id
        packet['who'] = text
        location = get_location(device_name)
        if location['message'] == 'ok':
            packet['where'] = location['loc']
        else:
            packet['where'] = "unknown location"
        packet['when'] = time.time()
        print(str(packet))
    else:
        pass
        # print("not moved")
    
GPIO.cleanup()
