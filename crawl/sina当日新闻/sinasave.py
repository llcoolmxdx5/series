import csv
import os


def code_transfer(string):
    replaces = ['"', '：', ' ', ' ', ':', '/', '<', '>', '?', '“', '”', '|', '*']
    for i in replaces:
        string = string.replace(i, '')
    return string


def gbk_cannot(string):
    replaces = ['记者', '新浪', '中新网', '澎湃新闻', '中国网', '新京报', '央视网', '海外网', '环球网', 
                '来源：', '新华社', '长安街知事']
    for i in replaces:
        string = string.replace(i, '')
    return string


def main(now_date, file_content, result_path):
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    with open(file_content, 'r', encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        while True:
            try:
                for row in reader:
                    title = code_transfer(row[0])
                    if len(title) < 2:
                        continue
                    if title[:4] == '新闻中心':
                        title = title[4:]
                    path = f'{result_path}\\{title}.txt'
                    if os.path.exists(path):
                        continue
                    content = []
                    l = row[1][1:-1].split(',')
                    num = 0
                    for p in l:
                        num += 1
                        if len(p) < 5:
                            continue
                        if '原标题' in p or '责任编辑' in p:
                            continue
                        if num < 2:
                            content.append(gbk_cannot(p[1:-1]))
                        else:
                            content.append(gbk_cannot(p[2:-1]))
                    content_str = '\n\n'.join(content)
                    if len(content) < 1:
                        continue
                    with open(path, 'w', encoding='utf-8') as f1:
                        f1.write(content_str)
                break
            except Exception as e:
                print(e)
