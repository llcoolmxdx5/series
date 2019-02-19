import csv
import requests
from random import shuffle
from os import mkdir
import os

read_filename = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\solomncontent.csv'
write_filename = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\content' + '\\'

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


def main():
    with open(read_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        while True:
            try:
                for row in reader:
                    title = code_transfer(row[0][:12])
                    path = write_filename + title
                    if os.path.exists(path):
                        continue
                    mkdir(path)
                    content = []
                    l = row[1][1:-1].split(',')
                    for p in l:
                        content.append(p[2:-5])
                    shuffle(content)
                    content = '\n\n'.join(content)
                    with open(path + '\\' + title + '.txt', 'w') as f1:
                        f1.write(content)

                    url = row[3]

                    pic_L = row[2]
                    if len(pic_L) > 2:
                        pic_s = pic_L[1:-1]
                        pic_L = pic_s.split(',')
                        for pic_url in pic_L:
                            content = html_download(pic_url, url)
                            if not content:
                                continue
                            with open(path + '\\'+pic_url[-8:-1], 'wb') as f:
                                f.write(content)
            except Exception as e:
                print(e)

