# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class ScrapyredistestPipeline(object):
    def process_item(self, item, spider):
        return item

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