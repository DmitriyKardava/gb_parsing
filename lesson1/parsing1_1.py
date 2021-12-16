import requests
import json

base_url = 'https://api.github.com'
user_name = 'DmitriyKardava'

r = requests.get(f'{base_url}/users/{user_name}/repos')
with open('data.json', 'w') as json_file:
    json.dump(r.json(), json_file)

for _i in r.json():
    print(_i['name'])
