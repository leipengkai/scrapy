import json
from scrapy_redis.spiders import RedisSpider
from ..items import InstagramItem

class MySpider(RedisSpider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    redis_key = 'instagram:start_urls'


    def parse(self, response):
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

        # while has_next:
        #     url = NEXT_URL.format(end_cursor)
        #     yield scrapy.Request(url, callback=self.parse)
