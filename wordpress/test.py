import csv
import sys

file_header = ['网站后台地址','用户名','密码','文件夹路径','关键词']
with open(sys.path[0]+'\\config.csv','w',encoding='gb18030') as csvfile:
    writer = csv.DictWriter(csvfile,file_header)
    writer.writeheader()
