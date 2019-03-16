import jieba

class Similarword:
    def __init__(self):
        with open('./similarword.txt', 'r', encoding='utf-8') as fr:
            self.word_dict = {}
            try:
                while True:
                    s = fr.readline()[:-1]
                    l1 = s.split(' ')
                    self.self.word_dict[l1[0]] = l1[1]
                    self.word_dict[l1[1]] = l1[0]
            except:
                pass

    def __del__(self):
        del self.word_dict

    def word_replace(self, body):
        seg_list = jieba.cut(body)
        s1 = ''
        for word in seg_list:
            result = self.word_dict.get(word, '')
            if result:
                s1 += result
                continue
            s1 += word
        return s1

    
    