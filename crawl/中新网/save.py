import csv
import os
from os import mkdir
from random import shuffle

import requests

from config import path1


def html_download(picurl, url):
    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    # request = Request(url, headers=headers)
    if 'http' in picurl:
        request_url = (picurl.strip())[1:-1]
    elif picurl[:4] == "'/cr":
        request_url = 'http://www.chinanews.com.cn' + picurl[1:-1]
        # print(request_url)
    else:
        index = url.rindex('/') + 1
        request_url = url[:index] + picurl[1:-1]
    try:
        res = requests.get(request_url, headers=headers)
    except:
        pass
    else:
        return res.content


def code_transfer(string):
    replaces = ['"', '：', ' ', ' ', ':', '/', '<', '>', '?', '“', '”', '|', '*']
    for i in replaces:
        string = ''.join(string.split(i))
    return string


def gbk_cannot(string):
    replaces = ['\u30fb', '\ufffd', '\u3000', '\n']
    for i in replaces:
        string = ''.join(string.split(i))
    return string

def main(file_content):
    with open(file_content, 'r', encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        while True:
            try:
                for row in reader:
                    title = code_transfer(row[0])[:-4]
                    if len(title) < 2:
                        continue
                    path = path1 + '\\' + title + '.txt'
                    if os.path.exists(path):
                        continue
                    content = []
                    l = row[1][1:-1].split(',')
                    num = 1
                    for p in l:
                        if len(p) < 5:
                            continue
                        if num == 1:
                            content.append(gbk_cannot(p[1:-5]))
                        else:
                            content.append(gbk_cannot(p[2:-5]))
                        num += 1
                    content = '\n\n'.join(content)
                    if len(content) < 20:
                        continue
                    with open(path, 'w') as f1:
                        f1.write(content)
                break
            except Exception as e:
                print(e)
