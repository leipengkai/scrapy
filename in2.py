""" -*- coding: utf-8 -*- """
import re
import json
import os
from lxml import etree
import requests
import click
from urllib import parse
import time

PAT = re.compile(r'queryId:"(\d*)?"', re.MULTILINE)
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/nois7/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36",
    "Host": "www.instagram.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "zh-CN,zh;q=0.8",
    "X-Instragram-AJAX": "1",
    "X-Requested-With": "XMLHttpRequest",
    "Upgrade-Insecure-Requests": "1",
}

# jso = {"id": "1179476381", "first": 12, "after": ""}
jso = {"id": "", "first": 12, "after": ""}

BASE_URL = "https://www.instagram.com"


# QUERY = "/morisakitomomi/"  # 森咲智美
QUERY = "/nois7/"
# QUERY = "/leipengkai/"  #

NEXT_URL = 'https://www.instagram.com/graphql/query/?query_hash={0}&variables={1}'

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
    个人主页,但滚动加载的内容攫取不到(没有登录不能加载json数据),但下载不了图片
    """
    click.echo('start...')
    try:
        all_imgs_url = []
        res =session.get(BASE_URL + QUERY, headers=headers, proxies=proxy)  # , verify=False)
        html = etree.HTML(res.content.decode())
        all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')  # 图片数据源
        query_id_url = html.xpath('//script[@crossorigin="anonymous"]/@src')  # query_id 作为内容加载
        click.echo(query_id_url)
        for a_tag in all_a_tags:
            if a_tag.strip().startswith('window._sharedData'):
                data = a_tag.split('= {')[1][:-1]  # 获取json数据块
                js_data = json.loads('{' + data, encoding='utf-8')
                user_id = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
                edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
                end_cursor = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
                has_next = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

                for edge in edges:
                    # if top_url and top_url == edge["node"]["display_url"]:
                        # in_top_url_flag = True
                        # break
                    click.echo(edge["node"]["display_url"])
                    # new_imgs_url.append(edge["node"]["display_url"])
                    # click.echo(qq.get(node["display_src"], proxies=proxy).status_code)

                    # 请求query_id
                    query_content =session.get(BASE_URL + query_id_url[3], headers=headers, proxies=proxy)
                    query_id_list = PAT.findall(query_content.text.encode('utf-8').decode('utf-8'))
                    for u in query_id_list:
                        click.echo(u)
                    # query_id = query_id_list[1]
                    query_id = "5b0222df65d7f6659c9b82246780caa7"

                    count = 0
                    # 更多的图片加载
                while has_next and count <= 1:
                    jso["id"] = user_id
                    jso["first"] = 12
                    jso["after"] = end_cursor
                    text = json.dumps(jso)
                    url = NEXT_URL.format(query_id, parse.quote(text))
                    print(session)
                    # 在没有登录的情况下,是获取不到json数据
                    res =session.get(url, headers=headers, proxies=proxy)
                    time.sleep(2)
                    html = json.loads(res.content.decode('utf-8'), encoding='utf-8')
                    has_next = html["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
                    end_cursor = html["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
                    edges = html["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
                    for edge in edges:
                        click.echo(edge["node"]["display_url"])
                        count += 1
                        # all_imgs_url.append(edge["node"]["display_url"])
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
