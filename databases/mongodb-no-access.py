#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
import argparse
import threading
import time

good=0
num=0

class Verfic:
    def __init__(self,ip,port,timeout):
        self.port=port
        self.ip=ip
        self.timeout=timeout
    def test(self):
        client=pymongo.MongoClient(self.ip,self.port,connectTimeoutMS=self.timeout)
        try:
            client.database_names()
        except Exception:
            return False
        else:
            return True
class Scanner:
    def __init__(self,rsource,wsource,port,timeout,threadnum):
        self.rsource=rsource
        self.wsource=wsource
        self.port=port
        self.timeout=timeout
        self.threadnum=threadnum
        self.content=self.rsource.read().split('\n')
        self.lock=threading.Lock()
        self.thread=[]
        self.content.remove("")
    def readip(self):
         if len(self.content)>0:
            ip=self.content.pop()
            return ip
         else:
             return False
    def send(self):
        global num
        global good
        #print(threading.currentThread().getName())
        while True:
            self.lock.acquire()
            ip=self.readip()
            if ip:
                num+=1               
                verfic=Verfic(ip,self.port,self.timeout)
                print ' %s Connecting %s ' % (threading.currentThread().getName(),ip)
                self.lock.release()
                result=verfic.test()
                if result:
                    self.lock.acquire()
                    good+=1
                    print ' Connect %s succed' % (ip)
                    self.wsource.write(ip+'\n')
                    self.lock.release()
            else:
                self.lock.release()
                break
    def start(self):
        for i in range(self.threadnum):
            self.thread.append(threading.Thread(target=self.send))
        for i in self.thread:
            i.start()
        for i in self.thread:
            i.join()
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--readfile',dest='readfile',type=str)
    parser.add_argument('--writefile',dest='writefile',type=str)
    parser.add_argument('--port',dest='port',default=27017,type=int)
    parser.add_argument('--timeout',dest='timeout',default=2500,type=int)
    parser.add_argument('--threadnum',dest='threadnum',default=5,type=int)
    args=parser.parse_args()
    readfile=args.readfile
    writefile=args.writefile
    port=args.port
    timeout=args.timeout
    threadnum=args.threadnum
    rsource=open(readfile,'r')
    wsource=open(writefile,'a')
    start=time.time()
    scanner=Scanner(rsource,wsource,port,timeout,threadnum)
    scanner.start()
    print 'sum:%d' % (num)
    print 'succed:%d' % (good)
    end=time.time()
    print 'scann time%.2fs' % (end-start)
    wsource.close()
    rsource.close()

