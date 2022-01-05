import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/komplekty/modulnye-shkafy/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photo', "//uc-variant-card/a[@class='image']/uc-image/img/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
