import redis
import telnetlib
import urllib.request
from bs4 import BeautifulSoup

r = redis.Redis(host='127.0.0.1', port=6379)

for d in range(1, 3):  # 采集1到2页
    scrapeUrl = 'http://www.xicidaili.com/nn/%d/' % d
    req = urllib.request.Request(scrapeUrl)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib.request.urlopen(req)
    html = response.read()

    bsObj = BeautifulSoup(html, "html.parser")

    for i in range(100):
        speed = float(bsObj.select('td')[6 + i * 10].div.get('title').replace('秒', ''))
        if speed < 0.2:  # 验证速度，只要速度在0.2秒之内的
            ip = bsObj.select('td')[1 + i * 10].get_text()
            port = bsObj.select('td')[2 + i * 10].get_text()
            ip_address = 'http://' + ip + ':' + port
            try:
                telnetlib.Telnet(ip, port=port, timeout=2)  # 用telnet对ip进行验证
            except:
                print('fail')
            else:
                print('sucess：' + ip_address)
                r.sadd('ippool', ip_address)  # 可用的ip导入到redis
                f = open('proxy_list.txt', 'a')
                f.write(ip_address + '\n')
                f.close()
