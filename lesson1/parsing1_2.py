import requests
import json
from config import token

api_url = 'https://api.github.com/user/repos'
user_name = 'DmitriyKardava'

r = requests.get(api_url, auth=(user_name, token))

with open('all_data.json', 'w') as json_file:
    json.dump(r.json(), json_file)

for _i in r.json():
    print(_i['name'])

