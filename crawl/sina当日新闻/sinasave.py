import csv
import os


def code_transfer(string):
    replaces = ['"', '：', ' ', ' ', ':', '/', '<', '>', '?', '“', '”', '|', '*']
    for i in replaces:
        string = ''.join(string.split(i))
    return string


def gbk_cannot(string):
    replaces = ['\u30fb', '\ufffd', '\u3000', '\n']
    for i in replaces:
        string = ''.join(string.split(i))
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
                        title = title[5:]
                    path = f'{result_path}\\{now_date}.txt'
                    if os.path.exists(path):
                        continue
                    content = []
                    l = row[1][1:-1].split(',')
                    num = 0
                    for p in l:
                        num += 1
                        if len(p) < 5:
                            continue
                        if num < 2:
                            content.append(gbk_cannot(p[1:-1]))
                        else:
                            content.append(gbk_cannot(p[2:-1]))
                    content = '\n\n'.join(content)
                    if len(content) < 20:
                        continue
                    with open(path, 'w') as f1:
                        f1.write(content)
                break
            except Exception as e:
                print(e)
