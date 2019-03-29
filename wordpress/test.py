import csv
import sys
import random
# file_header = ['网站后台地址','用户名','密码','文件夹路径']
# with open(sys.path[0]+'\\config.csv', 'w', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile,file_header)
#     writer.writeheader()


L1 = [row.split(',')[0] for row in open(sys.path[0]+r'\add.csv', 'r', encoding='gb18030')]
random.shuffle(L1)
# print(L)
L = [x for x in range(7)]
if len(L) < 8:
    L = L + L1[:8-len(L)]
print(L)
print(len(L))