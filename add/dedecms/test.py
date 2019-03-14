import os

path = r'D:\后端\python\series\add\dedecms'
result = [(i, os.stat(f'{path}\\{i}').st_mtime) for i in os.listdir(path)]
for i in sorted(result, key=lambda x: x[1], reverse=True):
    if i[0][-3:] == 'txt':
        title = i[0][:-4]
        path1 = path + i[0]
        print(path1)