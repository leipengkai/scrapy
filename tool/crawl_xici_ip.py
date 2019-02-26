# -*- coding: utf-8 -*-
import requests
from scrapy.selector import Selector
import pymysql
# from quoteturorial.quoteturorial.settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER

craete_table = """

CREATE TABLE `proxy_ip` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `ip` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        `port` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
        `speed` float(4.3) COLLATE utf8mb4_unicode_ci NOT NULL,
        `proxy_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    AUTO_INCREMENT=1 ;


"""
# dbparms = dict(
#     host=MYSQL_HOST,
#     db=MYSQL_DBNAME,
#     user=MYSQL_USER,
#     passwd=MYSQL_PASSWORD,
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor,
#     use_unicode=True,
# )
# 打开数据库连接
# conn = pymysql.connect(**dbparms)
conn = pymysql.connect(host='0.0.0.0',db='test',user='root',passwd='123456')


# 使用 cursor() 方法创建一个游标对象 cursor
cursor = conn.cursor()



def crawl_ips(pages):
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(pages):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")


        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:

            speed = ip_info[3]
            proxy_type = ip_info[2]
            if speed < 2:
                cursor.execute(
                    "insert proxy_ip(ip, port, proxy_type,speed ) VALUES('{0}', '{1}', '{2}', {3})".format(
                    ip_info[0], ip_info[1], proxy_type,speed
                    )
                )

                conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict,headers=headers)
        except Exception as e:
            print ("exce ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print  ("invalid ip and port")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()



if __name__ == "__main__":
    # print (crawl_ips(3))
    get_ip = GetIP()
    get_ip.get_random_ip()