# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from toripchanger import TorIpChanger

# from tool.crawl_xici_ip import GetIP


class QuoteturorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        ua = get_ua()
        request.headers.setdefault('User-Agent', get_ua())

# class RandomProxyMiddleware(object):
#     # 动态设置ip代理
#     def process_request(self, request, spider):
#         # request.meta["proxy"] = 'http://127.0.0.1:8118'
#         get_ip = GetIP()
#         ip = get_ip.get_random_ip()
#         print(ip)
#         request.meta["proxy"] = ip




# A Tor IP will be reused only after 10 different IPs were used.
ip_changer = TorIpChanger(reuse_threshold=10)


class ProxyMiddleware(object):
    _requests_count = 0

    def process_request(self, request, spider):
        self._requests_count += 1

        if self._requests_count > 4:
            self._requests_count = 0
            ip_changer.get_new_ip()

        request.meta['proxy'] = 'http://127.0.0.1:8118'
        spider.log('Proxy : %s' % request.meta['proxy'])
        # spider.log('request_count : %s' % str(self._requests_count))


from scrapy.http import HtmlResponse
class JSPageMiddleware(object):

    #通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "instagram1":
            url = request.url
            spider.browser.get(url)
            import time
            # time.sleep(3)
            # for i in range(2):
            #     spider.browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            #     time.sleep(3)
            # print ("访问:{0}".format(url))
            if url == "https://www.instagram.com/explore/tags/nois7/":
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)
