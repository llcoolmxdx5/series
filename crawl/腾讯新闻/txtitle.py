import requests
import re
from urllib.parse import urlencode
import csv
import multiprocessing
import threading
from pyquery import PyQuery as pq
from functools import partial

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
        return int(page) + 1
    except:
        return 1
    

def parse_html(html):
    doc = pq(html)
    aes = doc('h3.t a').items()
    for a in aes:
        yield a.attr('href'), a.text()


def save_to_csv(items, file_title):
    with open(file_title, "a", newline='', encoding='gb18030') as csvfile:
        # print(' 正在写入csv文件中.....')
        writer = csv.writer(csvfile)
        writer.writerow(items)


def start(page,key,file_title):
    try:
        html = html_download(page, key)
        print(f'正在抓取第{page}-第{page+1}')
        for items in parse_html(html):
            if '今日滚动新闻' in items[1]:
                continue
            save_to_csv(items, file_title)
    except Exception as e:
        print(e)


def main(key, file_title):
    html = html_download(750, key)
    page_total = parse_page(html)
    print(f'总计{page_total}0不到')
    #多线程
    pool = multiprocessing.Pool()
    # 多进程
    thread = threading.Thread(target=pool.map,args = (partial(start, key=key, file_title=file_title), 
                                                      [x for x in range(0, page_total*10, 10)]))
    thread.start()
    thread.join()

