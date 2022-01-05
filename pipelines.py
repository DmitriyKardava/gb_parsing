# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import os
from urllib.parse import urlparse
from urllib.parse import unquote
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class LmparserPipeline:
    def process_item(self, item, spider):
        return item


class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['name']}/{os.path.basename(urlparse(unquote(request.url)).path)}"
