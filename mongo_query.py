from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['insta2001']
users = db.instagram

name = input('Укажите имя пользователя: ')
print(f'Подписчики:')
for user in users.find({'$and': [{'source_name': name, 'type': 'following'}]}):
    pprint(user)

print(f'Подписки:')
for user in users.find({'$and': [{'source_name': name, 'type': 'follower'}]}):
    pprint(user)
