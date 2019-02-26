import os
import sys

path1 = r'D:\chengxv - 副本\后端\python\crawl\cnserch\solomn\content\《1937南京记忆》囊括\《1937南京记忆》囊括.txt'
def autokeyword(path):
    import jieba.analyse
    with open(path) as f:
        content = f.read()
    tags = jieba.analyse.extract_tags(content, topK=20, allowPOS=('ns', 'n', 'vn', 'v', 'i', 'l', 'nr', 'nt', 'nz'))
    return ','.join(tags)
    
keys = autokeyword(path1)
print(keys)