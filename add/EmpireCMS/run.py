import csv
import sys

from main import main

if __name__ == "__main__":
    with open(sys.path[0]+r'\config.csv', 'r', encoding='gb18030') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(row['网站后台地址']) < 2:
                print(f"网站后台地址为空,跳过该行")
                continue
            url = row['网站后台地址']
            user = row['用户名']
            password = row['密码']
            subcolumn_selector = row['是否选择子栏目']
            maincolumn_id = row['主栏目ID']
            subcolumn_id = row['子栏目ID']
            path = row['文件夹路径']
            try:
                main(url, user, password, subcolumn_selector, maincolumn_id, subcolumn_id, path)
            except:
                print(f'{url}出现错误 重试')
                main(url, user, password, subcolumn_selector, maincolumn_id, subcolumn_id, path)
