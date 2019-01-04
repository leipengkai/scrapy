""" -*- coding: utf-8 -*- """
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymysql
from twisted.enterprise import adbapi
from scrapy.conf import settings
import pymongo


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][:self.limit].rstrip() + '....'
            return item
        else:
            return DropItem('Missing Text')


class MysqlPipeline(object):
    """
    保存到mysql
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        # 实例化一个对象
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常


    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        pass
        # print(failure)


    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print(insert_sql, params)
        try:
            cursor.execute(insert_sql, params)
        except Exception as e:
            print(e)

    # def spider_closed(self, spider):
        # self.connection.close()

class InstagramImagePipeline(ImagesPipeline):
    '''自定义图片下载器,以图片url为路径保存图片'''

    def get_media_requests(self, item, info):
        '''发生图片下载请求,其中item['front_image_url']字段是scrapy中我们自定义的url字段,
        以数组的方式存储,遍历数组请求图片'''

        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

        def item_completed(self, results, item, info):
            # 将下载的图片路径（传入到results中）存储到 image_paths 项目组中，如果其中没有图片，我们将丢弃项目:
            image_path = [x['path'] for ok, x in results if ok]
            if not image_path:
                raise DropItem("Item contains no images")
            item['image_path'] = image_path
            return item



class MongodbPipeline(object):
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host,port=port,username='root',password='123456')

        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        data = dict(item)
        url = data.get('url')
        if 'name' in data:
            # 向指定的表里添加数据
            # self.post.insert(data)
            self.post.find_one_and_update({'url':url},{'$set':{'name':data.get('name')}},upsert=True,)
        else:
            self.post.update_one({'url':url},{'$set':
    {'detail':data.get('detail')}})
        return item