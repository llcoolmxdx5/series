import csv
import datetime
import multiprocessing
import re
import sys
import threading
from datetime import datetime, timedelta
from functools import partial
import time

import requests


def html_download(url):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    # request = Request(url, headers=headers)
    try:
        html = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        return None
    return html.json()


def parse_page(date, page):
    url = f'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&date={date}&k=&num=50&page={page}'
    html = html_download(url)
    datas = html['result']['data']
    for data in datas:
        pre_url = data['urls'][2:-2]
        url = ''
        for i in pre_url:
            if i != '\\':
                url += i
        title = data['title']
        yield title, url

def save_to_csv(items, file_title):
    with open(file_title, "a", newline='' ,encoding='gb18030') as csvfile:
        print(f'正在写{items[0]}')
        writer = csv.writer(csvfile)
        writer.writerow(items)


def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def start(page, now_date, file_title):
    for res in parse_page(now_date, page):
        save_to_csv(res, file_title)


def get_totalpage(date):
    now_day = datetime.today().date() - timedelta(days=0)
    pre_day = datetime.today().date() - timedelta(days=1)
    stime = int(time.mktime(time.strptime(str(now_day), '%Y-%m-%d')))
    etime = int(time.mktime(time.strptime(str(pre_day), '%Y-%m-%d')))
    url = f'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&date={date}&k=&num=50&page=1&etime={etime}&stime={stime}&ctime={stime}'
    html = html_download(url)
    total_page = html['result']['total']
    return int(total_page) // 50 + 1

def main(now_date, file_title):
    total_page = get_totalpage(now_date)
    #多线程
    pool = multiprocessing.Pool()
    # 多进程
    thread = threading.Thread(target=pool.map,args = (partial(start, now_date=now_date, file_title=file_title),
                                                     [x for x in range(1,total_page+1)]))
    thread.start()
    thread.join()

if __name__ == '__main__':
    # a = get_totalpage('2019-03-21')
    # print(a)
    print(datetime.today().date())
