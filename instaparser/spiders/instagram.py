import json
import re

import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instaparser.items import InstaparserItem
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login_name = 'Onliskill_udm'
    inst_login_pwd = '#PWD_INSTAGRAM_BROWSER:10:1642094301:ASZQAK3xQiN26pezmbNTERAktepuAKlWlqcVqr7z3rsE5QVlY3+nAifmia79/DHxjFYAEDdYBKj4jWG+n69gVxvObSIcbyeYMnhZQctoc6QcJo7R7ulkoaD18rDvHEaQm+dFbB28veuLCZFUtGll'
    parse_users = ['raslon', 'sochipress']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    friendship_url = 'https://i.instagram.com/api/v1/friendships/'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login_name, 'enc_password': self.inst_login_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):

        j_body = response.json()
        if j_body.get('authenticated'):
            for parse_user in self.parse_users:
                yield response.follow(f'/{parse_user}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': parse_user}
                                      )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12, 'search_surface': 'follow_list_page'}
        followers_url = f'{self.friendship_url}{user_id}/followers/?{urlencode(variables)}'
        following_url = f'{self.friendship_url}{user_id}/following/?{urlencode(variables)}'
        yield response.follow(followers_url,
                              callback=self.followers_parse,
                              cb_kwargs={'username': username, 'user_id': user_id, 'variables': variables},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        yield response.follow(following_url,
                              callback=self.following_parse,
                              cb_kwargs={'username': username, 'user_id': user_id, 'variables': variables},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        users = j_data.get('users')
        for user in users:
            yield InstaparserItem(source_id=user_id, source_name=username,
                                  user_id=user.get('pk'), username=user.get('username'),
                                  photo=user.get('profile_pic_url'),
                                  full_name=user.get('full_name'),
                                  pic_id=user.get('profile_pic_id'),
                                  type = 'follower')
        if j_data['big_list']:
            variables['max_id'] = variables.get('max_id', 0) + 12;
            followers_url = f'{self.friendship_url}{user_id}/followers/?{urlencode(variables)}'
            yield (response.follow(followers_url,
                                  callback=self.followers_parse,
                                  cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'}))

    def following_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        users = j_data.get('users')
        for user in users:
            yield InstaparserItem(source_id=user_id, source_name=username,
                                  user_id=user.get('pk'), username=user.get('username'),
                                  photo=user.get('profile_pic_url'),
                                  full_name = user.get('full_name'),
                                  pic_id = user.get('profile_pic_id'),
                                  type = 'following')
        if j_data['big_list']:
            variables['max_id'] = variables.get('max_id', 0) + 12;
            following_url = f'{self.friendship_url}{user_id}/following/?{urlencode(variables)}'

            yield (response.follow(following_url,
                                  callback=self.following_parse,
                                  cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'}))

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
