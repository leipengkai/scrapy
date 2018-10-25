""" -*- coding: utf-8 -*- """
import scrapy
# from urllib3 import parse
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    """
    攫取简单实例
    """
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        next_url = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next_url)
        yield scrapy.Request(url=url, callback=self.parse)
        # yield scrapy.Request(url=parse.urljoin(response.url,url), callback=self.parse)
