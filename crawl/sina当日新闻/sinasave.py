import csv
import os


def code_transfer(string):
    replaces = ['"', '：', ' ', ' ', ':', '/', '<', '>', '?', '“', '”', '|', '*']
    for i in replaces:
        string = ''.join(string.split(i))
    return string


def gbk_cannot(string):
    replaces = ['\u30fb', '\ufffd', '\u3000', '\n','\u2022', '\u22c5','\u25ba','\u25b7','\uf9dd','\xf6','\xb3',
                '\xba','\u2f0a','\xb4','\xc5','\u25aa','\u301c','\u2122','\uff89','\u2f08','\xae','\u2027','\xa0',
                '责任编辑', '记者','新浪','中新网','澎湃新闻','中国网','新京报','央视网','原标题','来源：']
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
                        if p[:3] == '原标题':
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
