# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.insta2001

    def write_to_db(self, item, collection_name):
        collection = self.mongobase[collection_name]
        try:
            collection.insert_one(item)
        except Exception as e:
            print(e, item)
            pass


    def process_item(self, item, spider):
        self.write_to_db(item, spider.name)
        return item



