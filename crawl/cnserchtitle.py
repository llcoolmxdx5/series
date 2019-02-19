import csv
from math import ceil
from sys import exit
from urllib.parse import quote

import requests
from pyquery import PyQuery as pq

file_name = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\solomntitle.csv'
ENCODING = 'utf-8'
KEYWORD = '时时彩'

def code_transfer(string):
    replaces = ['\u2022']
    for i in replaces:
        string.replace(i, '')
    return string


def html_download(page):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    # request = Request(url, headers=headers)
    url = 'http://sou.chinanews.com/search.do'
    data = {
        'q' : '%s' % KEYWORD,
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
        html = requests.post(url, headers=headers, data=data)
        html.encoding = ENCODING
    except:
        pass
    else:
        return html.text

def save_to_csv(items):
    with open(file_name, "a", newline='', encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(items)


def parse_data(html):
    doc = pq(html)
    aes = doc('li.news_title a').items()
    for a in aes:
        title = code_transfer(a.text())
        url = a.attr('href')
        yield title, url


def parse_page(html):
    doc = pq(html)
    page = doc('#search_rs_info > div:nth-child(2) > span').text()
    page = int(page.replace(',', ''))
    print('总页数：', page)
    return ceil(page / 10) * 10 + 1


def main():
    html = html_download(0)
    page_total = parse_page(html)
    if page_total == 1:
        exit('未找到相关文章')
    for page in range(0, page_total, 10):
        html = html_download(page)
        for item in parse_data(html):
            try:
                save_to_csv(item)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main() 
