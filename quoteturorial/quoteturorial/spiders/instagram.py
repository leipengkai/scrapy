# -*- coding: utf-8 -*-
import json
import time
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ..items import InstagramItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/explore/tags/nois7/']
    #
    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    #     super(InstagramSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     #当爬虫退出的时候关闭chrome
    #     print ("spider closed")
    #     self.browser.quit()

    def parse(self, response):
        # time.sleep(3)
        # for i in range(2):
        #     self.browser.execute_script(
        #         "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        #     time.sleep(3)
        has_next = False
        NEXT_URL = "https://www.instagram.com/explore/tags/nois7/?__a=1&max_id={0}"

        all_a_tags = response.xpath('//script[@type="text/javascript"]/text()')  # 图片数据源
        for a_tag in all_a_tags.extract():
            if a_tag.startswith('window._sharedData'):
                data = a_tag.split('= {')[1][:-1]  # 获取json数据块
                js_data = json.loads('{' + data, encoding='utf-8')
                edges = js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
                end_cursor = \
                js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"][
                    "end_cursor"]
                has_next = \
                js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"][
                    "has_next_page"]

                count = 0
                for edge in edges:
                    count += 1
                    image_url = edge["node"]["display_url"]
                    item = InstagramItem()
                    # item.__setattr__('image_urls',[image_url])
                    # item.image_urls = [image_url]
                    item['image_urls'] = [image_url]
                    yield item

        url = NEXT_URL.format(end_cursor)
        print('next::::',url)
        yield scrapy.Request(url, callback=self.parse_next)

    def parse_next(self,response):
        print('*'*100)
        time.sleep(2)
        # html = json.loads(response.content.decode('utf-8'), encoding='utf-8')
        html = json.loads(response.body_as_unicode())

        has_next = html["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"]
        end_cursor = html["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        edges = html["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        for edge in edges:
            image_url = edge["node"]["display_url"]
            item = InstagramItem()
            item['image_urls'] = [image_url]
            yield item
        if has_next:
            NEXT_URL = "https://www.instagram.com/explore/tags/nois7/?__a=1&max_id={0}"
            url = NEXT_URL.format(end_cursor)
            yield scrapy.Request(url, callback=self.parse_next)
