# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacncies2712


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['min'], item['max'], item['cur'] = self.process_salary_sj(item['salary'])
        # del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        min_zp = 0
        max_zp = 0
        cur_zp = ''
        if len(salary) == 7:
            min_zp = salary[1].replace(u'\xa0', '')
            max_zp = salary[3].replace(u'\xa0', '')
            cur_zp = salary[6]
        if len(salary) == 5:
            if salary[0].strip() == 'от':
                min_zp = salary[1].replace(u'\xa0', '')
            if salary[0].strip() == 'до':
                max_zp = salary[1].replace(u'\xa0', '')
            cur_zp = salary[3]
        try:
            min_zp = float(min_zp)
        except:
            pass
        try:
            max_zp = float(max_zp)
        except:
            pass
        return min_zp, max_zp, cur_zp

    def process_salary_sj(self, salary):
        min_zp = 0
        max_zp = 0
        cur_zp = ''
        if len(salary) == 5:
            _sal_summ = salary[2].split(u'\xa0')
            cur_zp = _sal_summ.pop(-1)
            if salary[0] == 'от':
                min_zp = ''.join(_sal_summ)
            if salary[0] == 'до':
                max_zp = ''.join(_sal_summ)
        if len(salary) == 9:
            min_zp = salary[0]
            max_zp = salary[4]
            cur_zp = salary[6]
        try:
            min_zp = float(min_zp)
        except:
            pass
        try:
            max_zp = float(max_zp)
        except:
            pass
        return min_zp, max_zp, cur_zp
