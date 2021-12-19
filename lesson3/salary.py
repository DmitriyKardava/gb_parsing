from pymongo import MongoClient


def get_vacancies(salary, exchange_rates):
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh']
    mongo_vacancies = db['vacancies']
    for vacancy in mongo_vacancies.find():
        if vacancy['salary_from']:
            _s = vacancy['salary_from'] * exchange_rates.get(vacancy['salary_cur']) if exchange_rates.get(vacancy['salary_cur'])\
                else vacancy['salary_from']
            if _s >= salary:
                print(vacancy)
                continue
        if vacancy['salary_to']:
            _s = vacancy['salary_to'] * exchange_rates.get(vacancy['salary_cur']) if exchange_rates.get(vacancy['salary_cur'])\
                else vacancy['salary_to']
            if salary <= _s:
                print(vacancy)
    client.close()


if __name__ == '__main__':
    salary = 100000
    exchange_rates = {'USD': 74.17, 'EUR': 83.37}
    get_vacancies(salary, exchange_rates)