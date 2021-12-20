from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlparse

client = MongoClient('127.0.0.1', 27017)
db = client['hh']

mongo_vacancies = db['vacancies']

main_url = 'https://hh.ru'
vacancy_to_search = 'python'
page = 0
params = {'fromSearchLine': 'true',
          'text': vacancy_to_search,
          'page': page}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
vacancy_list = []

while True:
    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    if response.ok and vacancies:
        print(f'Parsing page {page}')
        page += 1
        params['page'] = page
        for vacancy in vacancies:
            vacancy_data = {}
            salary_from = None
            salary_to = None
            salary_cur = None
            name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            if name:
                url = name.get('href')
                name = name.text
                hh_id = urlparse(url).path.split('/')[-1]
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if salary:
                salary = salary.text.replace('\u202f', '').split(' ')
                if len(salary) == 3 and salary[0] == 'от':
                    salary_from = salary[1]
                    salary_cur = salary[2]
                if len(salary) == 3 and salary[0] == 'до':
                    salary_to = salary[1]
                    salary_cur = salary[2]
                if len(salary) == 4:
                    salary_from = salary[0]
                    salary_to = salary[2]
                    salary_cur = salary[3]
                if salary_from:
                    try:
                        salary_from = float(salary_from)
                    except:
                        salary_cur = None
                if salary_to:
                    try:
                        salary_to = float(salary_to)
                    except:
                        salary_cur = None
            else:
                salary = None

            site = main_url
            vacancy_data['name'] = name
            vacancy_data['salary_from'] = salary_from
            vacancy_data['salary_to'] = salary_to
            vacancy_data['salary_cur'] = salary_cur
            vacancy_data['url'] = url
            vacancy_data['hh_id'] = hh_id
            vacancy_data['site'] = site
            vacancy_list.append(vacancy_data)
    else:
        break
doc_count = 0;
if db['vacancies'].estimated_document_count() == 0:
    mongo_vacancies.insert_many(vacancy_list)
    print("В базе нет вакансий")
    doc_count = len(vacancy_list)
else:
    print(f"В базе {db['vacancies'].estimated_document_count()} вакансий")
    for vacancy in vacancy_list:
        x = mongo_vacancy = mongo_vacancies.find_one(vacancy)
        if not x:
            try:
                mongo_vacancies.insert_one(vacancy)
                doc_count += 1
                print(vacancy)
            except Exception as e:
                print(e)
                pass
print(f"Добавлено {doc_count} вакансий")
client.close()
