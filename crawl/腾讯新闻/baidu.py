import requests
import re
from urllib.parse import urlencode
import csv
import multiprocessing
import threading


WRITE_TO_FILE = 'baiduurl.csv'
FILEHEADER = ['URL',]
keyword = 'python'

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


def parse_html(html):
    regxp = r'<h3.*?href="(.*?)".*?</h3>'
    result = re.findall(regxp, html ,re.S)
    for url in result:
        yield url


def write_csv_header(fileheader):
    with open(WRITE_TO_FILE, "a",newline='') as csvfile:
        writer = csv.DictWriter(csvfile, FILEHEADER)
        writer.writeheader()


def save_to_csv(items):
    with open(WRITE_TO_FILE, "a",newline='') as csvfile:
        # print(' 正在写入csv文件中.....')
        writer = csv.writer(csvfile)
        writer.writerow(items)


def main(page):
    raw_url = 'https://www.baidu.com/s?'
    parms = {
        'wd' : keyword,
        'pn' : page
    }
    url = raw_url + urlencode(parms)
    html = html_download(url)
    print(page)
    for url in parse_html(html):
        save_to_csv([url])


if __name__ == '__main__':
    #多线程
    write_csv_header(FILEHEADER) 
    pool = multiprocessing.Pool()
    # 多进程
    thread = threading.Thread(target=pool.map,args = (main, [x for x in range(0, 760, 10)]))
    thread.start()
    thread.join()
