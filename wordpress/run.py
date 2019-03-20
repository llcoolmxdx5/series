import csv
import sys

from main import main

date = '2019-03-19'

if __name__ == "__main__":
    with open(sys.path[0]+r'\config.csv', 'r', encoding='gb18030') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(row['网站后台地址']) < 2:
                print("网站后台地址为空,跳过该行")
                continue
            url = row['网站后台地址']
            user = row['用户名']
            password = row['密码']
            path = row['文件夹路径'] + '\\' + date
            Key = row['关键词']
            main(url, user, password, path, Key)
