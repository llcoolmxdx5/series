import csv
import multiprocessing
import threading
import time

import requests
from pyquery import PyQuery as pq

from txconfig import path


def html_download(url):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    try:
        html = requests.get(url, headers=headers, timeout=(5, 18))
        html.encoding = 'gb2312'
    except:
        print(f'错误{url}')
    else:
        return html.text


def save_to_csv(items, file_content):
    with open(file_content, "a", newline='', encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(items)


def parse_data(html, url):
    doc = pq(html)
    title = doc('title').text()
    if title[-7:] == '_新闻_腾讯网':
        title = title[:-7]
    content_p = []
    pes = doc('#Cnt-Main-Article-QQ > p').items()
    for p in pes:
        if 'var flash_vid' in p.text():
            continue # 去除插入的flash
        if 'strong#truth' in p.text():
            continue # 去除事实+
        if 'var related_video_info' in p.text():
            continue # 去除插入的腾讯视频代码
        if len(p.text()) < 10:
            continue
        content_p.append(p.text())
    return title, content_p, url


def start(url, file_content):
    try:
        html = html_download(url)
        items = parse_data(html, url)
        print(f'抓取{items[0]}成功')
        save_to_csv(items, file_content)
    except Exception as e:
        print(e)


def main(key, file_content):
    global file_title
    file_title = f'{path}\\腾讯新闻{key}title.csv'
    with open(file_title, 'r', encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        d = {}
        for row in reader:
            if min(len(row[1]),len(row[0])) < 10:
                continue
            d[f'{row[0]}'] = row[1]
    L = []
    for dkey,dvalue in d.items():
        L.append(dvalue)
    del d
    pool = multiprocessing.Pool()
    for url in L:
        pool.apply_async(start, (url, file_content))
    print(f'读取{file_title},保存到{file_content}')
    pool.close()
    pool.join()
    print(f'抓取{key}结束')
