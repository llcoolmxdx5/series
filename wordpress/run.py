import csv
import sys
from datetime import datetime, timedelta

from main import main
from main1 import main as main1

date = str(datetime.today().date() - timedelta(days=1))

if __name__ == "__main__":
    with open(sys.path[0]+r'\config.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(row['网站后台地址']) < 2:
                print("网站后台地址为空,跳过该行")
                continue
            url = row['网站后台地址']
            user = row['用户名']
            password = row['密码']
            path = row['文件夹路径'] + '\\' + date
            # try:
            #     main(url, user, password, path)
            # except Exception as e:
            #     print(e)
            #     main(url, user, password, path)
            try:
                main1(url, user, password, path)
            except Exception as e:
                print(e)
                main1(url, user, password, path)
