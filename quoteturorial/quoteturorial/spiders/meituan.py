# -*- coding: utf-8 -*-
import time
import scrapy
from urllib.parse import urlparse
from selenium import webdriver
from quoteturorial.items import MeituanItem 


class MeituanSpider(scrapy.Spider):
    """
    美团全部分类
    """
    name = 'meituan'
    allowed_domains = ['www.meituan.com','gz.meituan.com','meituan.com']
    start_urls = ['https://www.meituan.com/']

    # def start_requests(self):
    #     ...

    def __init__(self):
        """
        无界面版chrome使用方法
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")

        # 设置chromedriver不加载图片
        # prefs = {"profile.managed_default_content_settings.images":2}
        # chrome_options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/local/bin/chromedriver')
        self.driver = browser
        print("spider init")

    def parse(self, response):
        """
        selenium加载动态内容后使用 scrapy shell调试:
        使用scrapy crawl meituan,代替scrapy shell ...
        """
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        # 只能使用上一层的循环
        # urls = response.xpath('//a[@class="link nav-text"]/@href').extract()
        # names = response.xpath('//a[@class="link nav-text"]/text()').extract()
        # for i in range(len(urls)):

            # item = MeituanItem()
            # url = urls[i]
            # item['url'] = url
            # item['name'] = names[i]
            # yield item




        # pychram调试
        url = response.url
        self.driver.get(url)
        time.sleep(2)
        self.driver.find_element_by_xpath("html/body/div/div/a").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("html/body/div/div/div[2]/p/a[3]").click()
        time.sleep(2)


        # u = self.driver.find_elements_by_xpath('//*[@id="react"]/div/div/div[1]/div[1]/div/div[2]/ul/li[1]/span/span/a')
        l = self.driver.find_elements_by_xpath('//*[@id="react"]/div/div/div[1]/div[1]/div/div[2]/ul/li/span/span/a')
        for i in l:

            item = MeituanItem()
            url = i.get_attribute('href')
            item['url'] = url
            item['name'] = i.text

            next_url = response.urljoin(url)
            print('kk')
            print(next_url)
            # yield scrapy.Request(url=urlparse(str(url)),callback=self.parse_detail)
            yield item
            yield scrapy.Request(url=url, callback=self.parse_detail)

        ress = response.xpath('//li[@class="nav-li"]')
        for res in ress:
            name = res.css('.link.nav-text::text').extract()
            url = res.css('.link.nav-text::attr(href)').extract()
            # name = res.css('.link.nav-text::text').extract_first()
            # url = res.css('.link.nav-text::attr(href)').extract_first()

        # for res in ress:
            # names = res.xpath('//a[@class="link nav-text"]')
            # names = res.xpath('./a[@class="link nav-text"]') # 不行
            # for i in names:
                # print(i.extract())

    def parse_detail(self, response):
        url = response.url
        print('jj')
        print(url)
        detail = response.xpath('//*[@id="app"]/section/div/div[2]/div[1]/div/div')
        d = {}
        for i in detail:
            print('888')
            detail_name = i.css('.classification::text').extract_first()
            # all_a = i.css('a[href*]="https://gz.meituan.com/meishi/"').extract()
            # 所有的 不分开
            # hrefs = i.css('a[href*="http://gz.meituan.com/meishi/"]::attr(href)').extract()
            # a_names = i.css('a[href*="http://gz.meituan.com/meishi/"]::text').extract() 
            
            
            hrefs = i.xpath('./ul/li/a[contains(@href,"http://gz.meituan.com/meishi/")]/@href').extract()
            a_names = i.xpath('./ul/li/a/text()').extract()
            if hrefs:
                d_d = dict(zip(a_names, hrefs))
                d.update({detail_name:d_d})

            print(detail_name,hrefs,a_names)

        item = MeituanItem()
        item['url'] = url
        item['detail'] = d
        yield item


    # def spider_closed(self, spider):
    #     #当爬虫退出的时候关闭chrome
    #     print("spider closed")
    #     self.driver.quit()
