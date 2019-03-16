import csv
import multiprocessing
import re
import sys
import threading
from functools import partial

import requests
from pyquery import PyQuery as pq


def html_download(url):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    # request = Request(url, headers=headers)
    try:
        html = requests.get(url, headers=headers, timeout=(5, 18))
        html.encoding = 'utf-8'
    except:
        print('错误', url)
    else:
        return html.text


def parse_html(html, url):
    doc = pq(html)
    title = doc('h1').text()

    content_L = []
    pes = doc('#artibody p').items()
    for p in pes:
        if len(p.text()) < 10:
            continue
        content_L.append(p.text())
    if not content_L:
        pes = doc('#article p').items()
        for p in pes:
            if len(p.text()) < 10:
                continue
            content_L.append(p.text())
            
    return title, content_L, url


def save_to_csv(items, file_content):
    with open(file_content, "a", newline='', encoding='gb18030') as csvfile:
        print(f'正在写{items[0]}中')
        writer = csv.writer(csvfile)
        writer.writerow(items)


def start(url, file_content):
    try:
        html = html_download(url)
        item = parse_html(html, url)
        save_to_csv(item, file_content)
    except:
        pass


def main(file_title, file_content):
    urls = []
    with open(file_title, 'r', encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                if len(row[1]) < 10:
                    continue
                if row[1][:4] != 'http':
                    continue
                if row[1] not in urls:
                    urls.append(row[1])
            except:
                pass
    #多线程
    pool = multiprocessing.Pool()
    # 多进程
    thread = threading.Thread(target=pool.map, args = (partial(start, file_content=file_content), urls))
    thread.start()
    thread.join()


if __name__ == "__main__":
    url = 'https://news.sina.com.cn/c/2019-03-16/doc-ihsxncvh2920505.shtml'
    html = html_download(url)
    item = parse_html(html, url)
    print(item)