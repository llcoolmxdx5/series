import jieba

word_dict = {}
def get_dicionary():
    global word_dict
    with open('../nlp/similarword.txt', 'r', encoding='utf-8') as fr:
        try:
            while True:
                s = fr.readline()[:-1]
                l1 = s.split(' ')
                word_dict[l1[0]] = l1[1]
                word_dict[l1[1]] = l1[0]
        except:
            pass

def nlp_create(s):
    seg_list = jieba.cut(s)
    s1 = ''
    for word in seg_list:
        result = word_dict.get(word, '')
        if result:
            s1 += result
            continue
        s1 += word
    return s1
get_dicionary()
    
    