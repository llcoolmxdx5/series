import csv
import sys
import random
import os
# file_header = ['网站后台地址','用户名','密码','文件夹路径']
# with open(sys.path[0]+'\\config.csv', 'w', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile,file_header)
#     writer.writeheader()

def get_link():
    path = f'{sys.path[0]}\\urls'
    urls_path = os.listdir(path)
    random.shuffle(urls_path)
    path1 = f'{path}\\{urls_path[0]}'
    with open(path1, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        L = []
        for row in reader:
            L.append(row[0])
        random.shuffle(L)
    return f'<a href="{L[0]}" rel="nofollow">乐都城</a>'
print(get_link())