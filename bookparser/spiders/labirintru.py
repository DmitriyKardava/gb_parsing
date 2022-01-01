import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem
from urllib.parse import urlparse

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
#    start_urls = ['https://www.labirint.ru/books/']
    start_urls = ['https://www.labirint.ru/genres/965/',
                 'https://www.labirint.ru/genres/3000/',
                 'https://www.labirint.ru/genres/1852/',
                 'https://www.labirint.ru/genres/1850/',
                 'https://www.labirint.ru/genres/2137/',
                 'https://www.labirint.ru/genres/2993/',
                 'https://www.labirint.ru/genres/2386/',
                 'https://www.labirint.ru/genres/3066/',
                 'https://www.labirint.ru/genres/11/'
                 ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@id='catalog']/.//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        discount = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        authors = response.xpath("//div[@class='authors']/a/text()").getall()
        url = response.url
        _id = urlparse(url).path.split('/')[-2]
        yield BookparserItem(name=name, price=price, discount=discount, rating=rating, authors=authors, url=url, _id=_id)
