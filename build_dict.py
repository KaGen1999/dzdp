import requests
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont
import hashlib
import time
from config import connect
import pymysql
import pickle


def download_css(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    r = requests.get(url, headers)
    fonts = re.findall('//s3plus\.meituan\.net/v1/mss_.{1,50}/font/.{1,20}\.woff', r.text)
    tag_class = re.findall('} \.(.*?){', r.text)
    d = {}
    if len(fonts) == len(tag_class):
        for u, t in zip(fonts, tag_class):
            d[t] = 'http:' + u
    return d


def build_dict(d):
    db = connect()
    cursor = db.cursor()
    tag_dict = {}
    for k in d.keys():
        url = d[k]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        r = requests.get(url, headers=headers)
        woff_file_name = k + '_' + url.split('/')[-1].replace('.woff', '')
        with open('./font_files/' + woff_file_name + '.woff', 'wb')as f:
            f.write(r.content)
        print(woff_file_name, '下载完成')
        font = TTFont('./font_files/' + woff_file_name + '.woff')
        font.saveXML('./font_files/' + woff_file_name + '.xml')
        with open('./font_files/' + woff_file_name + '.xml', 'r', encoding='utf-8')as f:
            t = f.read()
        md5_list = {}
        soup = BeautifulSoup(t, 'xml')
        ttg_list = soup.find_all('TTGlyph')
        for ttg in ttg_list:
            tar = re.findall(r'name=".*?"', str(ttg))[0]
            name = re.findall(r'name="(.*?)"', str(ttg))[0]
            result = str(ttg).replace(tar, '')
            md5_code = hashlib.md5(result.encode(encoding='utf-8')).hexdigest()
            sql = "SELECT word FROM woff WHERE hash_code=%s"
            args = (md5_code,)
            cursor.execute(sql, args)
            result = cursor.fetchall()
            if len(result) > 0:
                word = result[0][0]
                # md5_list[name.replace('uni', '\\u').encode('utf-8').decode('unicode-escape')] = word
                md5_list[name.replace('uni', '@@@').encode('utf-8').decode('unicode-escape')] = word
        tag_dict[k] = md5_list
        # break
    return tag_dict


def get_dict(url, headers):
    r = requests.get(url, headers=headers)
    page_source = r.text
    svg_css_url = 'http:' + re.findall('//s3plus.meituan.net/.*?/svgtextcss/.*?css', page_source)[0]
    d = download_css(svg_css_url)
    tag_dict = build_dict(d)
    print(tag_dict)

    data = pickle.dumps(tag_dict)
    with open('./dict/dict.pkl', 'wb')as f:
        f.write(data)
    print('字典已经生成')


if __name__ == '__main__':
    url = 'http://www.dianping.com/nanping/ch10'
    headers = {
        'Host': 'www.dianping.com',
        # cookie自行配置
        'Cookie': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    get_dict(url, headers)
