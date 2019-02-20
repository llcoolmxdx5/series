import os
import sys
path = r'D:\web前端\39\03-1 京东电商项目\jd\images'
def read_file(path1): 
    path1 = path1 + '\\'
    list2 = os.listdir(path1)
    # for i in list2:
    #     if i[-3:] == 'txt':
    #         title = i[:-4]
    #         path2 = path1 + '\\' + i
    # with open(path2, 'r') as f:
    #     keyword = f.readline()[:-1]
    #     summary = f.readline()[:-1]
    #     L = [f'<style>body{{font-size: 14px;}}</style>']
    #     for i in f.readlines():
    #         if len(i) < 4:
    #             continue
    #         L.append(f'<span>　　{i[:-1].strip()}</span><br/>')
    #         L.append(f'<span>　　</span><br/>')
    L1 = []
    for i in list2:
        if i[-3:] in ['jpg','png', 'gif']:
            L1.append(path1+i)
    return L1
l = read_file(path)
print(len(l))