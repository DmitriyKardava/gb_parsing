from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from urllib.parse import urlparse
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from config import email, passwd


def exist_by_key(iterable, key, value):
    for index, dict_ in enumerate(iterable):
        if key in dict_ and dict_[key] == value:
            return True
    return False


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://mail.ru/')
element = driver.find_element(By.NAME, 'login')
element.send_keys(email)
element = driver.find_element(By.XPATH, "//button[@data-testid='enter-password']")
ActionChains(driver).move_to_element(element).click(element).perform()
element = driver.find_element(By.NAME, 'password')
element.send_keys(passwd)
element = driver.find_element(By.XPATH, "//button[@data-testid='login-to-mail']")
ActionChains(driver).move_to_element(element).click(element).perform()
element = driver.find_element(By.XPATH, "//div[@class='letter-list letter-list_has-letters']")

all_letters = []
_last_url = ''
while True:
    letters = element.find_elements(By.XPATH, ".//a[contains(@class, 'js-letter-list-item')]")
    if letters[-1].get_attribute('href') == _last_url:
        break
    _last_url = letters[-1].get_attribute('href')
    for letter in letters:
        _url = letter.get_attribute('href')
        # Здесь надо провалиться внутрь url и распарсить письмо
        if _url and not exist_by_key(all_letters, 'url', _url):
            mail = {}
            _id = urlparse(_url).path
            _from = letter.find_element(By.XPATH, ".//div[contains(@class, 'llc__item_correspondent')]/span")\
                .get_attribute('title')
            _subj = letter.find_element(By.XPATH, ".//span[contains(@class, 'llc__subject')]").text
            _date = letter.find_element(By.XPATH, ".//div[contains(@class, 'llc__item_date')]").text
            mail['_id'] = _id
            mail['url'] = _url
            mail['from'] = _from
            mail['subj'] = _subj
            mail['date'] = _date
            all_letters.append(mail)
    ActionChains(driver).move_to_element(letters[-1]).perform()
driver.close()

client = MongoClient('127.0.0.1', 27017)
db = client['mail']
mongo_letters = db['letters']

try:
    mongo_letters.insert_many(all_letters, ordered=False)
except BulkWriteError as e:
    pass

client.close()
