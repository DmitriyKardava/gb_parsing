# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def clear_name(name):
    if not name:
        return None
    return name.strip()

def clear_price(value):
    if not value:
        return None
    value = value.replace('\xa0', '')
    try:
        value = int(value)
    except:
        pass
    finally:
        return value


class LmparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(clear_name), output_processor=TakeFirst(), default='null')
    photo = scrapy.Field(default='null')
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst(), default='null')
    url = scrapy.Field(output_processor=TakeFirst(), default='null')
