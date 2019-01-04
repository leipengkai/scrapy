# -*- coding: utf-8 -*-
import os

import scrapy

from username.items import UsernameItem

class YimanwuSpider(scrapy.Spider):
    name = 'yimanwu'
    allowed_domains = ['www.yimanwu.com']
    # start_urls = ['http://www.yimanwu.com/']
    basic_url = "https://www.yimanwu.com/nvsheng/list_47_{}.html"
    start = 201  # 0,80,201
    start_urls = [basic_url.format(str(start))]

    def parse(self, response):
        item = UsernameItem()

        namelist = response.xpath("//div[@class=\'list\']/ul/li")
        for each in namelist:
            name = each.xpath("p/text()").extract()[0]
            print(name)
            # with open(os.path.normpath(os.path.join(os.getcwd(),'username/spiders/scrapyname')) ,'a') as f:
            #     f.write(name + '\n')

            item['username'] = name
            yield item

        self.start +=1
        print(self.start)
        if self.start > 320:
            return
        yield scrapy.Request(self.basic_url.format(str(self.start)), callback=self.parse)

