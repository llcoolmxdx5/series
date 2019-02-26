import csv
from random import shuffle

import requests

from nlptest import nlp_create, word_dict
from sql_test import insert_dede, db

read_filename = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\solomncontent.csv'

def code_transfer(string):
    replaces = ['"', '：', ' ', ' ', ':', '/', '<', '>', '?', '“', '”', '|', '*']
    for i in replaces:
        string = ''.join(string.split(i))
    return string

def main():
    with open(read_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        L = []
        while True:
            try:
                for row in reader:
                    if row[0][:12] not in L:
                        L.append(row[0][:12])
                    else:
                        continue
                    title = code_transfer(row[0][:12])
                    content = []
                    l = row[1][1:-1].split(',')
                    for p in l:
                        replace_string = nlp_create(p[2:-5])
                        content.append(replace_string)
                    shuffle(content)
                    content = '\n\n'.join(content)
                    if len(content) < 100:
                        continue
                    insert_dede(title, content)
            except Exception as e:
                print(e)
                break

if __name__ == "__main__":
    main()
    db.close()

