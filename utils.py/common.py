import csv
import os
import random
import sys

import requests

from series.config import DISORDER


def save_img():
    pass


def save2txt(read_path, write_path, encoding):
    '''
    :param: read_path: csv路径名 
    :param: write_path: 文件夹路径名 
    :param: encoding: csv编码

    ['title', ['','sfsdg','aDSAD']]保存为多个文件夹下的txt文本  
    '''
    L = []
    with open(read_path, 'r', encoding=encoding) as csvfile:
        reader = csv.reader(csvfile)
        while True:
            try:
                for row in reader:
                    if len(row[0]) < 2:
                        continue
                    if len(row[1]) < 5:
                        continue
                    if row not in L:
                        L.append(row)
                break
            except Exception as e:
                print(e)
    for j in L:
        try:
            title = ''
            for i in j[0]:
                if i not in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                    title += i
            path = write_path + '\\' + title
            if os.path.exists(path):
                continue
            os.mkdir(path)
            with open(path + '\\' + title + '.txt', 'a+', encoding=encoding) as f:
                f.write(j[0])
                f.write('\r\n')
                # 处理文章为一个列表
                content = []
                l = j[1][1:-1].split(',')
                for p in l:
                    if len(p) < 5:
                        continue
                    content.append(p[2:-1])
                # 乱序
                if DISORDER:
                    random.shuffle(content)
                content = '\n\n'.join(content)
                f.write(content)
        except:
            pass
    del L


def html_download(url, encoding, num_retries=5):
    headers = {'User-Agent': "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
    # request = Request(url, headers=headers)
    try:
        html = requests.get(url, headers=headers, timeout=5)
        html.encoding = encoding
    except Exception as e:
        if num_retries > 0:
            html_download(url, encoding=encoding, num_retries=num_retries-1)
        print(e)
    else:
        return html.text


def save_to_csv(write_path, items):
    with open(write_path, "a+", newline='', encoding='gb18030') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(items)
