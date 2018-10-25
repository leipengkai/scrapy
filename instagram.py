# -*- coding: utf-8 -*-

import json
from lxml import etree
import requests
import click

headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/_8_jjini/",
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

BASE_URL = "https://www.instagram.com/leipengkai/"
# BASE_URL = "https://www.instagram.com/nois7/"
BASE_URL = "https://www.instagram.com/leipengkai/saved/"

proxy = {
    'http': 'http://127.0.0.1:8118',
    'https': 'http://127.0.0.1:8118'
}


def crawl():
    click.echo('start')
    try:
        res = requests.get(BASE_URL, headers=headers, proxies=proxy)
        html = etree.HTML(res.content.decode())
        all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')
        for a_tag in all_a_tags:
            if a_tag.strip().startswith('window._sharedData'):
                data = a_tag.split('= {')[1][:-1]  # 获取json数据块
                js_data = json.loads('{' + data, encoding='utf-8')
                # edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
                edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_saved_media"]["edges"]
                for edge in edges:
                    # if top_url and top_url == edge["node"]["display_url"]:
                        # in_top_url_flag = True
                        # break
                    click.echo(edge["node"]["display_url"])
                    # new_imgs_url.append(edge["node"]["display_url"])
                click.echo('ok')
    except Exception as e:
        raise e


if __name__ == '__main__':
    crawl()
