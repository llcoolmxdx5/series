import csv
import multiprocessing
import random
import threading
import time
from sys import exit

import requests
from pyquery import PyQuery as pq

from config import path, keyword


def html_download(url):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    try:
        html = requests.get(url, headers=headers)
        html.encoding = 'gb2312'
        return html.text
    except Exception as e:
        print(e)
        return ''


def save_to_csv(items, file_content):
    with open(file_content, "a", newline='', encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(items)


def parse_data(html, url):
    doc = pq(html)
    title = doc('title').text()
    # 获取文章内容
    # 第一类
    content_p = [] #用来保存文章段落
    ps = doc('div.left_zw p').items()
    for p in ps:
        content_p.append(p.text()+'\n\n')
    # 第二类
    if len(content_p) == 0:
        ps = doc('#Zoom p').items()
        for p in ps:
            content_p.append(p.text()+'\n\n')
    # 第三类
    if len(content_p) == 0:
        ps = doc('#ad0 p').items()
        for p in ps:
            content_p.append(p.text()+'\n\n')
    # 第四类
    if len(content_p) == 0:
        ps = doc('table tr td div p').items()
        for p in ps:
            content_p.append(p.text()+'\n\n')
 
    # 获取文章图片
    img_urls = [] # 用来保存图片链接
    # 第一类
    imgs = doc('div.left_ph img').items()
    for img in imgs:
        img_urls.append(img.attr('src'))
    # 第二类
    if len(img_urls) == 0:
        imgs = doc('div.left_zw p img').items()
        for img in imgs:
            img_urls.append(img.attr('src'))
    # 第三类
    if len(img_urls) == 0:
        imgs = doc('#content img').items()
        for img in imgs:
            img_urls.append(img.attr('src'))

    return title, content_p, img_urls, url


def start(url, file_content):
    try:
        html = html_download(url)
        i = 1
        while not html or len(html) < 2000:
            print(f'抓取{url}失败,重试第{i}次')
            time.sleep(i)
            html_download(url)
            if i >= 5:
                print(f'抓取{url}失败,跳过')
                break
            i += 1
        items = parse_data(html, url)
        save_to_csv(items, file_content)
    except Exception as e:
        print(e)


def main(key, file_content):
    global file_title
    file_title = path + '\\' + key + 'title.csv'
    with open(file_title, 'r', encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        L = []
        for row in reader:
            if 'shipin' in row[1]:
                continue
            L.append(row[1])
    pool = multiprocessing.Pool()
    for url in L:
        pool.apply_async(start, (url, file_content))
    print(f'读取{file_title},保存到{file_content}')
    pool.close()
    pool.join()
    print(f'抓取{key}结束')
