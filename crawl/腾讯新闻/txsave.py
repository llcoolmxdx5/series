import csv
import os
import time

from config import path1


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


def main(key, file_content):
    path2 = f'{path1}\\{key}'
    if not os.path.exists(path2):
        os.mkdir(path2)
    print(f'保存{key}相关腾讯新闻到{path2}开始')
    with open(file_content, 'r', encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        while True:
            try:
                for row in reader:
                    title = code_transfer(row[0])
                    if len(title) < 2:
                        continue
                    path = f'{path2}\\{title}.txt'
                    if os.path.exists(path):
                        continue
                    content = []
                    l = row[1][1:-1].split(',')
                    num = 0
                    for p in l:
                        num += 1
                        if len(p) < 5:
                            continue
                        if num < 2:
                            content.append(gbk_cannot(p[1:-1]))
                        else:
                            content.append(gbk_cannot(p[2:-1]))
                    content = '\n\n'.join(content)
                    if len(content) < 20:
                        continue
                    with open(path, 'w') as f1:
                        f1.write(content)
                break
            except Exception as e:
                print(e)
    print(f'保存{key}相关腾讯新闻到{path2}完成')

if __name__ == "__main__":
    main('时时彩', r'D:\新建文件夹\腾讯新闻时时彩content.csv')

