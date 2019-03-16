import csv
import sys

from main import main

if __name__ == "__main__":
    with open(sys.path[0]+r'\config.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(row['网站后台地址']) < 2:
                print(f"网站后台地址为空,跳过该行")
                continue
            url = row['网站后台地址']
            user = row['用户名']
            password = row['密码']
            path = row['文件夹路径']
            try:
                main(url, user, password, path)
            except:
                print(f'{url}出现错误 重试')
                main(url, user, password, path)
