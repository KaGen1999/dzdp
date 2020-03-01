import requests
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont
import hashlib
import time
from config import connect
import pymysql
import pickle

url = 'http://www.dianping.com/nanping/ch10'
headers = {
    'Host': 'www.dianping.com',
    # cookie自行配置一下
    'Cookie': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
page_source = r.text.replace('&#x', ';@@@')
with open('./dict/dict.pkl', 'rb')as f:
    tag_dict = pickle.loads(f.read())
print(tag_dict)
soup = BeautifulSoup(page_source, 'lxml')
shop_list = soup.find('div', id='shop-all-list').find('ul').find_all('li')


for shop in shop_list:
    tag_addr = shop.find('div', class_='tag-addr')
    shop_name = shop.find('h4').text
    shop_type = ''
    shop_type_list = shop.find('div', class_='tag-addr').find('a').find('span').text.split(';')
    for j in shop_type_list:
        if j in tag_dict['tagName'].keys():
            shop_type = shop_type + tag_dict['tagName'][j]
        else:
            shop_type = shop_type + j
    print(shop_name)
    print(shop_type)
