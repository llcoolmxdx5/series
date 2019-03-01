import csv
import multiprocessing
import threading
import time
from math import ceil
from sys import exit
from urllib.parse import quote
from urllib import error
import requests
from pyquery import PyQuery as pq

from config import keyword, path

file_title = path + '\\' + 'title.csv'

def code_transfer(string):
    replaces = ['\u2022']
    for i in replaces:
        string.replace(i, '')
    return string


def html_download(page, key):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
    # request = Request(url, headers=headers)
    url = 'http://sou.chinanews.com/search.do'
    # data = {'q': f'{quote(key)}','ps': 10,'start': page,'type': '','sort': '_score',
    #     'time_scope': 0,'channel': 'all','adv': 1,'day1': '','day2': '','field': '','creator': ''}
    data = {
        'q' : f'{key}',
        'ps' : 10,
        'start' : page,
        'type' : '',
        'sort' : 'pubtime', # _scope 按相关度
        'time_scope' : 0,
        'channel' : 'all', # yl 娱乐
        'adv' : 1,
        'day1' : '',
        'day2' : '',
        'field' : '',
        'creator' : '',
    }
    try:
        res = requests.post(url, headers=headers, data=data)
        res.encoding = 'utf-8'
        return res.text
    except Exception:
        return ''



def save_to_csv(items):
    global file_title
    with open(file_title, "a", newline='', encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(items)


def parse_data(html):
    doc = pq(html)
    aes = doc('li.news_title a').items()
    for a in aes:
        title = a.text()
        url = a.attr('href')
        yield title, url


def parse_page(html):
    doc = pq(html)
    page = doc('#search_rs_info > div:nth-child(2) > span').text()
    if len(page) < 4:
        page = int(page)
    else:
        page = int(page.replace(',', ''))
    print('总页数：', page)
    return ceil(page / 10) * 10 + 1


def start(key, page_total):
    global file_title
    file_title = path + '\\' + key + 'title.csv'
    for page in range(0, page_total, 10):
        print(f'正在抓取{page}/{page_total}')
        try:
            time.sleep(1)
            html = html_download(page, key)
            i = 1
            while not html or len(html) < 2000:
                print(f'抓取{page}失败,重试第{i}次')
                time.sleep(i)
                html_download(0, key)
                if i >= 5:
                    print(f'抓取失败')
                    break
                i += 1
            for item in parse_data(html):
                try:
                    save_to_csv(item)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


def main():
    # pool = multiprocessing.Pool()
    # # 多进程
    # thread = threading.Thread(target=pool.map, args = (start, [x for x in keyword]))
    # thread.start()
    # thread.join()
    for key in keyword:
        html = html_download(0, key)
        time.sleep(1)
        i = 1
        while not html or len(html) < 2000:
            print(f'抓取失败,重试第{i}次')
            time.sleep(i)
            html_download(0, key)
            if i > 20:
                print(f'抓取失败')
                break
            i += 1
        page_total = parse_page(html)
        if page_total == 1:
            continue
        start(key, page_total)
