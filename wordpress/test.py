import csv
import sys
import random
# file_header = ['网站后台地址','用户名','密码','文件夹路径','关键词']
# with open(sys.path[0]+'\\config.csv','w',encoding='gb18030') as csvfile:
#     writer = csv.DictWriter(csvfile,file_header)
#     writer.writeheader()
L = []
with open(sys.path[0]+r'\keyword.txt', 'r',encoding='utf-8') as f:
    for j in f.readlines():
        L.append(j[:-1])
# for i in L:
#     s = i.split(',')
#     title = s[0]
#     content_key = s[1:]
#     print(title)
#     print(content_key)
random.shuffle(L)

s = L[0].split(',')
title = s[0]
content_key = s[1:]
print(title)
print(content_key)