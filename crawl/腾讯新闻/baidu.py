import requests
import re
from urllib.parse import urlencode
import csv
import multiprocessing
import threading
from pyquery import PyQuery as pq
from config import path, path1, keyword

WRITE_TO_FILE = 'baiduurl.csv'
file_title = path + '\\' + 'title.csv'

def html_download(page, key):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    # request = Request(url, headers=headers)
    raw_url = 'https://www.baidu.com/s?'
    parms = {
        'wd' : f'site:news.qq.com {key}',
        'pn' : page
    }
    url = raw_url + urlencode(parms)
    try:
        html = requests.get(url, headers=headers, timeout=(5, 18))
        html.encoding = 'utf-8'
    except:
        print('错误', url)
    else:
        return html.text


def parse_page(html):
    doc = pq(html)
    page = doc('#page > strong > span.pc').text()
    try:
        return int(page)
    except:
        return 0
    

def parse_html(html):
    doc = pq(html)
    aes = doc('h3.t a').items()
    for a in aes:
        yield a.attr('href'), a.text()


def save_to_csv(items):
    global file_title
    with open(file_title, "a", newline='', encoding='utf-8') as csvfile:
        # print(' 正在写入csv文件中.....')
        writer = csv.writer(csvfile)
        writer.writerow(items)


def start(page,key=''):
    try:
        html = html_download(page, key)
        print(f'正在抓取第{page}')
        for items in parse_html(html):
            save_to_csv(items)
    except Exception as e:
        print(e)


def main(key):
    global file_title
    file_title = path + '\\' + '腾讯新闻' + key + 'title.csv'
    html = html_download(750, key)
    page_total = parse_page(html)
    print(f'总计{page_total}')
    #多线程
    pool = multiprocessing.Pool()
    # 多进程
    thread = threading.Thread(target=pool.map,args = (start, [x for x in range(0, page_total*10, 10)]))
    thread.start()
    thread.join()

if __name__ == '__main__':
    main('新闻')
    # html = html_download(750, '彩彩')
    # page_total = parse_page(html)
    # print(page_total)
