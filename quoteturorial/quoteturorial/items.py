# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into quotes(text, author)VALUES (%s, %s)"""
        # params = (self.text, self.author)  # 第一次可以的,但之后再运行时,就会有错
        params = (self['text'], self['author'])

        return insert_sql, params

        # create_table = """CREATE TABLE `quotes` (
        # `id` int(11) NOT NULL AUTO_INCREMENT,
        # `text` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        # `author` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        # PRIMARY KEY (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    # AUTO_INCREMENT=1 ;
    # """

class InstagramItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_path = scrapy.Field()