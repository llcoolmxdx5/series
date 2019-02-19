import csv
import multiprocessing
import random
import threading
from sys import exit

import requests
from pyquery import PyQuery as pq

file_name_write = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\solomncontent.csv'
file_name_read = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\solomntitle.csv'

def html_download(url):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    try:
        html = requests.get(url, headers=headers)
        html.encoding = 'gb2312'
    except:
        pass
    else:
        return html.text


def save_to_csv(items):
    with open(file_name_write, "a", newline='', encoding='gb18030') as csvfile:
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


def start(url):
    try:
        html = html_download(url)
        items = parse_data(html, url)
        save_to_csv(items)
    except Exception as e:
        print(e)


def main():
    with open(file_name_read, 'r') as csvfile:
        reder = csv.reader(csvfile)
        L = []
        for row in reder:
            if 'shipin' in row[1]:
                continue
            L.append(row[1])
    pool = multiprocessing.Pool()
    # 多进程
    thread = threading.Thread(target=pool.map, args = (start, [x for x in L]))
    thread.start()
    thread.join()


if __name__ == "__main__":
    main()
