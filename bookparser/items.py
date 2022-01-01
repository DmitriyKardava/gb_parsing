# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    rating = scrapy.Field()
    authors = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()