import jieba
import sys

class Similarword:
    def __init__(self):
        with open(sys.path[0]+'\\similarword.txt', 'r', encoding='utf-8') as fr:
            self.word_dict = {}
            try:
                while True:
                    s = fr.readline()[:-1]
                    l1 = s.split(' ')
                    self.self.word_dict[l1[0]] = l1[1]
                    self.word_dict[l1[1]] = l1[0]
            except:
                pass

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

s = '''
格隆汇3月13日丨韩国娱乐圈近日的热点“胜利事件”持续发酵，随着警方的深入调查，已从单纯的夜总会员工殴打客户事件，逐渐被揭出更多惊人内部。
韩国偶像团体BIGBANG成员胜利担任夜店Burning Sun董事，疑似向外籍投资者提供色情招待。且据相关证言显示，Burning Sun夜店偷偷给女顾客下药并让客人实施性侵，已成为有组织的行为。
同时，有媒体还曝出，胜利、韩国歌手郑俊英以及FTISLAND组合成员崔钟勋在群聊中多次共享偷拍到的不雅视频，视频当事人包括多位韩国偶像歌手。
受“胜利事件”牵连，韩国各大娱乐公司股价受到重创，YG娱乐本周内股价已下跌17%，市值蒸发逾1300亿韩元(约合7.7亿元人民币)。
韩国证券交易所12日甚至将YG娱乐指定为“抛售过热”股票，以防止抛售行为过度集中。
'''

similar = Similarword()
s1 = similar.word_replace(s)
print(s1)