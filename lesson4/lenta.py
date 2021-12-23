from lxml import html
import requests
from pprint import pprint
from urllib.parse import urlparse, urlunparse
from pymongo import MongoClient
import hashlib
import datetime

def get_id_for_dict(dict):
    _str = ''.join(["'%s':'%s';"%(key, val) for (key, val) in sorted(dict.items())])
    return hashlib.sha1(_str.encode('utf-8')).hexdigest()


def add_news(all_news):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    mongo_news = db['lenta']
    for news in all_news:
        x = mongo_news.find_one({'hash': news.get('hash')})
        if not x:
            news['created_at'] = datetime.datetime.now()
            mongo_news.insert_one(news)
            pprint(news)
    client.close()


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
news_url = 'https://lenta.ru/'
response = requests.get(news_url, headers=header)
dom = html.fromstring(response.text)
response.close()
all_news = []
lenta_news = dom.xpath("//div[contains(@class,'topnews')]//a[contains(@class,'_topnews')]")
for item in lenta_news:
    news = {}
    text = item.xpath("./div/span/text()|./div/h3/text()")[0]
    url = urlparse(item.xpath("./@href")[0])
    if not url.netloc:
        url = urlunparse(['https', 'lenta.ru', url.path, '', '', ''])
        source = 'lenta.ru'
    else:
        source = url.netloc
        url = urlunparse(url)
    date = item.xpath(".//time/text()")[0]
    news['text'] = text
    news['url'] = url
    news['date'] = date
    news['source'] = source
    news['hash'] = get_id_for_dict(news)
    all_news.append(news)
add_news(all_news)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
news_url = 'https://yandex.ru/news/'
response = requests.get(news_url, headers=header)
dom = html.fromstring(response.text)
response.close()
all_news = []
yandex_news = dom.xpath("//div[contains(@class,'news-top-flexible-stories')]")
for item in yandex_news:
    news = {}
    source = item.xpath(".//span[contains(@class,'mg-card-source__source')]//a/text()")[0]
    text = item.xpath(".//h2[contains(@class, 'mg-card__title')]/a/text()")[0].replace('\xa0', ' ')
    url = item.xpath(".//h2[contains(@class, 'mg-card__title')]/a/@href")[0]
    date = item.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")[0]
    news['text'] = text
    news['url'] = url
    news['date'] = date
    news['source'] = source
    news['hash'] = get_id_for_dict(news)
    all_news.append(news)
add_news(all_news)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
news_url = 'https://news.mail.ru/'
response = requests.get(news_url, headers=header)
dom = html.fromstring(response.text)
response.close()
all_news = []
mail_news = dom.xpath("//table[contains(@class,'daynews__inner')]//td/div/a/@href")
for item in mail_news:
    news = {}
    response = requests.get(item, headers=header)
    dom = html.fromstring(response.text)
    response.close()
    news_id = urlparse(item).path.split('/')[2]
    _mail_news = dom.xpath(f"//div[@data-news-id='{news_id}']")
    for _item in _mail_news:
        source = _item.xpath(".//a/@href")[0]
        text = _item.xpath(".//span[@class='hdr__text']/h1/text()")[0]
        url = item
        date = _item.xpath("//span/@datetime")
        news['text'] = text
        news['url'] = url
        news['date'] = date
        news['source'] = source
        news['hash'] = get_id_for_dict(news)
        all_news.append(news)
add_news(all_news)
