from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_url = 'https://hh.ru'
vacancy_to_search = 'python'
page = 1
params = {'fromSearchLine': 'true',
          'text': vacancy_to_search,
          'page': page}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
vacancy_list = []
while True:
    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    if response.ok:
        print(f'Parsing page {page}')
        page += 1
        params['page'] = page
        dom = bs(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancies:
            vacancy_data = {}
            salary_from = None
            salary_to = None
            salary_cur = None
            name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            if name:
                url = name.get('href')
                name = name.text
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
            vacancy_data['site'] = site
            vacancy_list.append(vacancy_data)
    else:
        break

pprint(vacancy_list)
