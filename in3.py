""" -*- coding: utf-8 -*- """
import re
import json
import os
from lxml import etree
import requests
import click
from urllib import parse
import time

headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/nois7/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36" ,
    "Host": "www.instagram.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "X-Instragram-AJAX": "1",
    "X-Requested-With": "XMLHttpRequest",
    "Upgrade-Insecure-Requests": "1",
}

# jso = {"id": "1179476381", "first": 12, "after": ""}
jso = {"id": "", "first": 12, "after": ""}

BASE_URL = "https://www.instagram.com"


QUERY = "/explore/tags/nois7/"

NEXT_URL = "https://www.instagram.com/explore/tags/nois7/?__a=1&max_id={0}"

proxy = {
    'http': 'http://127.0.0.1:8118',
    'https': 'http://127.0.0.1:8118'
}

try:
    import cookielib
except:
    import http.cookiejar as cookielib
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="instcookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载")

def crawl():
    """
    个人标签,但下载不了图片
    """
    click.echo('start...')
    try:
        all_imgs_url = []
        res =session.get(BASE_URL + QUERY, headers=headers, proxies=proxy)  # , verify=False)
        session.cookies.save()
        html = etree.HTML(res.content.decode())
        all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')  # 图片数据源
        query_id_url = html.xpath('//script[@crossorigin="anonymous"]/@src')  # query_id 作为内容加载
        for a_tag in all_a_tags:
            if a_tag.strip().startswith('window._sharedData'):
                data = a_tag.split('= {')[1][:-1]  # 获取json数据块
                js_data = json.loads('{' + data, encoding='utf-8')
                edges = js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
                end_cursor = js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
                has_next = js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"]


                count = 0
                for edge in edges:
                    # if top_url and top_url == edge["node"]["display_url"]:
                        # in_top_url_flag = True
                        # break
                    count += 1
                    image_url = edge["node"]["display_url"]
                    with open("images/{0}.jpg".format(str(count)),"wb") as f:
                        image_res =requests.get(image_url, headers=headers, proxies=proxy)
                        # response = requests.get("https://scontent-hkg3-2.cdninstagram.com/vp/81645d7b3109738d138d1b40480070f4/5C4552F8/t51.2885-15/e35/37222787_282372445675216_6242591018907074560_n.jpg",headers=headers,proxies=proxy)
                        f.write(image_res.content)
                        f.close()

                    click.echo(image_url)
                while has_next :
                    url = NEXT_URL.format(end_cursor)
                    res =session.get(url, headers=headers, proxies=proxy)
                    # time.sleep(2)
                    html = json.loads(res.content.decode('utf-8'), encoding='utf-8')
                    has_next = html["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"]
                    end_cursor = html["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
                    edges = html["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
                    for edge in edges:
                        click.echo(edge["node"]["display_url"])
                        count += 1
                        # all_imgs_url.append(edge["node"]["display_url"])
                    click.echo(count)
                click.echo('ok')
    except Exception as e:
        raise e

def instagram_login(username, password):
    # resp = session.get('http://instagram.com/' + username)
    # tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
    # tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
    # owner_data = json.loads(tmp2)['entry_data']['ProfilePage'][0]['user']
    data = {'username': username, 'password': password}
    # i = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers, proxies=proxy)
    # i = session.post('https://www.instagram.com/accounts/login/?source=auth_switcher', data=data, headers=headers, proxies=proxy)
    # i = session.post('https://www.instagram.com/accounts/login/?source=desktop_nav', data=data, headers=headers, proxies=proxy)
    i = session.post('https://www.instagram.com/accounts/login/', data=data, headers=headers, proxies=proxy)
    session.cookies.save()
    # login_url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
if __name__ == '__main__':
    crawl()
