# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books0101

    def process_item(self, item, spider):
        try:
            print(item['price'])
            item['price'] = float(item['price'])
        except:
            pass
        try:
            item['discount'] = float(item['discount'])
        except:
            pass
        collection = self.mongobase[spider.name]
        collection.update_one({'_id': item['_id']}, {'$set': item}, upsert=True)
        return item
