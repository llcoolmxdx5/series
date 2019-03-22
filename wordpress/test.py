import csv
import sys
import random
file_header = ['网站后台地址','用户名','密码','文件夹路径']
with open(sys.path[0]+'\\config.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile,file_header)
    writer.writeheader()
