from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import hashlib


def get_id_for_dict(dict):
    _str = ''.join(["'%s':'%s';"%(key, val) for (key, val) in sorted(dict.items())])
    return hashlib.sha1(_str.encode('utf-8')).hexdigest()


def add_goods(_goods):
    client = MongoClient('127.0.0.1', 27017)
    db = client['mvideo']
    _goods = db['trends']
    for _good in goods:
        x = _goods.find_one({'hash': _good.get('hash')})
        if not x:
            _goods.insert_one(_good)
    client.close()


driver = webdriver.Chrome()
driver.get('https://mvideo.ru')
# element = driver.find_element(By.TAG_NAME, 'mvid-shelf-group').location_once_scrolled_into_view
element = driver.find_element(By.TAG_NAME, 'mvid-shelf-group')
actions = ActionChains(driver)
actions.move_to_element(element).perform()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button/div/span[@class='title'"
                                                                      " and contains(.,'В тренде')]/../.."))).click()
names = element.find_elements(By.XPATH, ".//div[contains(@class, 'product-mini-card__name')]")
prices = element.find_elements(By.XPATH, ".//div[contains(@class, 'product-mini-card__price')]"
                                         "//span[@class='price__main-value']")
print(len(prices))
goods = []
for i in range(len(names)):
    good = {'name': names[i].text, 'price': prices[i].text}
    good['hash'] = get_id_for_dict(good)
    goods.append(good)
add_goods(goods)
driver.close()
