# -*- coding: utf-8 -*-
import re
import scrapy
from username.items import THZItem


class Thz2Spider(scrapy.Spider):
    name = 'thz2'
    allowed_domains = ['thzvv.net']
    # basic_url = "http://thz2.cc/forum-181-{}.html"  # 1~378 fqdc
    # basic_url = "http://thz2.cc/forum-220-{}.html"  # 1~492 dedc
    basic_url = "http://thzvv.net/forum-181-{}.html" # 381  
    start = 1 
    start_urls = [basic_url.format(str(start))]

    def parse(self, response):
        item = THZItem()

        urllist = response.xpath('//a[@class="s xst"]')        
        for each in urllist:
            name = each.xpath('text()').extract_first()
            url = each.xpath('@href').extract_first()
            # result = re.search('立花瑠莉',name)
            # result = re.search('水野朝陽',name)
            # result = re.search('新道ありさ',name) 
            # result = re.search('新垣结衣',name) 
            result = re.search('みづなれい',name) 
            if result:
                # url = 'http://thz2.cc/' + url
                url = 'http://thzvv.net/' + url
                item['url'] = url
                item['name'] = name
                yield item



        self.start +=1
        print(self.start)
        if self.start > 381:
            return
        yield scrapy.Request(self.basic_url.format(str(self.start)), callback=self.parse)
