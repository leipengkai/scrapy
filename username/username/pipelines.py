# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings

import pymongo

class UsernamePipeline(object):
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host,port=port,username='root',password='123456')

        # 指向指定的数据库
        mdb = client[dbname]
        # mdb.authenticate("root", "123456", mechanism='SCRAM-SHA-1')
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.insert(data)
        return item

class THZPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME_THZ']

        client = pymongo.MongoClient(host=host,port=port,username='root',password='123456')

        mdb = client[dbname]
        self.post = mdb[settings['MONGODB_DOCNAME_THZ']]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
